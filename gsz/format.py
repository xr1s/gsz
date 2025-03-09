import enum
import functools
import html
import io
import os
import typing
import unicodedata


@typing.runtime_checkable
class SRGameData(typing.Protocol):
    @functools.cached_property
    def _extra_effect_config_names(self) -> set[str]: ...


class Syntax(enum.Enum):
    Plain = 1
    Terminal = 2
    MediaWiki = 3
    MediaWikiPretty = 4


class GenderOrder(enum.Enum):
    Preserve = 0
    Male = 1
    Female = 2


class State(enum.Enum):
    """
    除了无格式的纯文本外，主要有三类
    * 格式化字符串，有以下形式 #1 #2[f2]% #3[i] #4[m]
    * 类似 XML 的某种 DSL，有以下形式 <u> </i> <color=#0000> <size=20> <size=+2>
    * 某种特殊的变量 DSL，有以下形式
        {BIRTH}
        {F#女性开拓者分支} {M#男性开拓者分支}
        {RUBY_B#注音内容}对话内容{RUBY_E}
        {TEXTJOIN#编号}
    """

    HashSign = 2
    """HashSign 表示格式化字符串中的第一个井号字符，表示后面有格式化字符串内容"""
    ParamNum = 3
    """ParamNum 表示格式化字符串井号和左方括号中间的数字，指引用参数列表中的第几个参数"""
    Specifier = 4
    """
    Specifier 表示方括号之间的格式化串，可能为
    * 空（不会进入本状态）
    * f 后接一个数字，表示保留多少位小数的浮点数
    * i 表示整数，可能有千位分隔符
    * m 表示将数字 1,000,000 表示成「一百万」等，各语言对应的缩写形式
    """
    ParamEnd = 5
    """ParamEnd 表示格式化字符串中的右方括号，需要再读一个字符决定后续走向 Percent 还是 Literal"""
    Escaping = 6
    """目前只有 \\n 这一个需要转义的"""
    TagLKey = 10
    """TagLKey 表示类 XML 标识中的标签名，比如 <u> </i> <size=20>，中的 u i size"""
    TagLVal = 11
    """TagLVal 表示类 XML 标识比如 <color=#000000> <size=20> 中的 #000000 20"""
    TagText = 12
    """TagText 表示标签内部的正文"""
    TagRBra = 13
    """
    TagRBra 表示 TagText 中间出现的 <

    注意可能是嵌套的 Tag，比如 <align="right"><i>这里是正文</i></align>
    所以后续可能转移到下一个 TagLVal 中
    """
    TagSlash = 14
    """
    XML Tag 形式的标识，可能有以下标签 <u> <i> <color=#000000> <size=20> <size=+2>
    TagSlash 表示 </i> 的 /
    """
    VarKey = 20
    """VarKey 记录比如 {BIRTH} <RUBY_B#注音内容> 中的 BIRTH RUBY_B"""
    VarVal = 21
    """VarKey 记录比如 {F#女性开拓者分支} {RUBY_B#注音内容} 中的 女性开拓者分支 注音内容"""


class InlineBlock(enum.Enum):
    Inline = False
    Block = True


class Formatter:
    def __init__(
        self,
        *,
        syntax: Syntax | None = None,
        game: SRGameData | None = None,
        gender_order: GenderOrder = GenderOrder.Preserve,
    ):
        self.__game = game
        self.__syntax: Syntax = syntax if syntax is not None else Syntax.Plain
        self.__states: list[State] = []
        self.__texts: list[io.StringIO] = [io.StringIO()]
        self.__param_num: int = 0
        self.__specifier: str = ""
        self.__keys: list[io.StringIO] = []
        self.__vals: list[io.StringIO] = []
        self.__close_tag: io.StringIO = io.StringIO()
        self.__parameter: tuple[float | str, ...] = ()
        self.__is_inline_block: InlineBlock = InlineBlock.Inline
        # var 相关状态
        self.__gender_order = gender_order
        self.__f_text = ""
        self.__m_text = ""
        self.__ruby = ""

    def __push(self, s: str):
        match self.__syntax:
            case Syntax.Plain | Syntax.Terminal:
                _ = self.__texts[-1].write(s)
            case Syntax.MediaWiki | Syntax.MediaWikiPretty:
                for char in s:
                    if char in (" ", "\xa0"):
                        _ = self.__texts[-1].write("&nbsp;")
                    elif char == "\n":
                        _ = self.__texts[-1].write("<br />")
                    else:
                        _ = self.__texts[-1].write(html.escape(char))

    def __display_block_afterward(self):
        if self.__is_inline_block == InlineBlock.Block and self.__syntax == Syntax.MediaWikiPretty:
            _ = self.__texts[-1].write("\n")
        self.__is_inline_block = InlineBlock.Inline

    def __feed_text(self, char: str):
        match char:
            case "#":
                self.__display_block_afterward()
                self.__states.append(State.HashSign)
            case "<":
                self.__display_block_afterward()
                self.__states.append(State.TagLKey)
                self.__keys.append(io.StringIO())
                self.__vals.append(io.StringIO())
                self.__texts.append(io.StringIO())
            case "{":
                self.__display_block_afterward()
                self.__states.append(State.VarKey)
                self.__keys.append(io.StringIO())
                self.__vals.append(io.StringIO())
            case "\\":
                self.__states.append(State.Escaping)
            case "\xa0":
                self.__display_block_afterward()
                self.__push(" ")
            case _:
                self.__display_block_afterward()
                self.__push(char)

    def __feed_hash_sign(self, char: str) -> None:
        if char.isdigit():
            self.__param_num = self.__param_num * 10 + ord(char) - ord("0")
            self.__states[-1] = State.ParamNum
            return
        _ = self.__states.pop()
        self.__push("#")
        self.__push(char)

    def __feed_param_num(self, char: str) -> None:
        if char.isdigit():
            self.__param_num = self.__param_num * 10 + ord(char) - ord("0")
            return None
        if char == "[":
            self.__states[-1] = State.Specifier
            return None
        if char == "%":
            return self.__flush_format(True)
        self.__flush_format()
        return self.__feed_text(char)

    def __feed_specifier(self, char: str) -> None:
        if char == "]":
            self.__states[-1] = State.ParamEnd
            return
        self.__specifier += char

    def __feed_param_end(self, char: str) -> None:
        if char == "%":
            self.__flush_format(True)
            return
        self.__flush_format()
        self.__feed_text(char)

    def __feed_escaping(self, char: str) -> None:
        _ = self.__states.pop()
        if char == "n":
            if self.__is_inline_block == InlineBlock.Block:
                return  # 前一个是 block 标签，需要手动无视一次回车
            self.__push("\n")
            if self.__syntax == Syntax.MediaWikiPretty:
                _ = self.__texts[-1].write("\n")
            self.__is_inline_block = InlineBlock.Inline
            return
        self.__push("\\")
        self.__push(char)

    def __feed_tag_l_key(self, char: str) -> None:
        if char == "<":
            # 有 <<<</align> 这种特殊情况
            # 说明前序也是 <，直接 push 没问题
            self.__push("<")
            return
        if char == "=":
            tag = self.__keys[-1].getvalue()
            if not self.__is_known_tag(tag):
                _ = self.__states.pop()
                _ = self.__keys.pop()
                _ = self.__vals.pop()
                _ = self.__texts.pop()
                self.__push("<")
                self.__push(tag)
                self.__push("=")
                return
            self.__states[-1] = State.TagLVal
            return
        if char == ">":
            tag = self.__keys[-1].getvalue()
            if not self.__is_known_tag(tag):
                _ = self.__states.pop()
                _ = self.__keys.pop()
                _ = self.__vals.pop()
                _ = self.__texts.pop()
                self.__push("<")
                self.__push(tag)
                self.__push(">")
                return
            self.__states[-1] = State.TagText
            return
        _ = self.__keys[-1].write(char)

    def __feed_tag_l_val(self, char: str) -> None:
        if char == ">":
            self.__states[-1] = State.TagText
            return
        _ = self.__vals[-1].write(char)

    def __feed_tag_text(self, char: str) -> None:
        if char == "<":
            self.__states[-1] = State.TagRBra
            return
        self.__feed_text(char)

    def __feed_tag_r_bra(self, char: str) -> None:
        if char == "/":
            self.__states[-1] = State.TagSlash
            return
        self.__display_block_afterward()
        if char == ">":
            self.__push("<>")
            self.__states[-1] = State.TagText
            return
        self.__states[-1] = State.TagText
        self.__states.append(State.TagLKey)
        key = io.StringIO(char)
        _ = key.seek(1)
        self.__keys.append(key)
        self.__vals.append(io.StringIO())
        self.__texts.append(io.StringIO())

    def __feed_tag_slash(self, char: str) -> None:
        if char == ">":
            tag = self.__close_tag.getvalue()
            self.__close_tag = io.StringIO()
            if tag == self.__keys[-1].getvalue():
                self.__flush_tag()
                return
            self.__push("</")
            self.__push(tag)
            self.__push(">")
            self.__states[-1] = State.TagText
            return
        _ = self.__close_tag.write(char)

    def __feed_var_key(self, char: str) -> None:
        if char == "}":
            var = self.__keys[-1].getvalue()
            if not self.__is_known_var(var):
                _ = self.__states.pop()
                _ = self.__keys.pop()
                _ = self.__vals.pop()
                _ = self.__texts.pop()
                self.__push("{")
                self.__push(var)
                self.__push("}")
                return
            self.__flush_var()
            return
        if char == "#":
            var = self.__keys[-1].getvalue()
            if not self.__is_known_var(var):
                _ = self.__states.pop()
                _ = self.__keys.pop()
                _ = self.__vals.pop()
                _ = self.__texts.pop()
                self.__push("{")
                self.__push(var)
                self.__push("#")
                return
            self.__states[-1] = State.VarVal
            self.__push("")
            return
        _ = self.__keys[-1].write(char)

    def __feed_var_val(self, char: str) -> None:
        if char == "}":
            self.__flush_var()
            return
        _ = self.__vals[-1].write(char)

    @staticmethod
    def __do_format(specifier: str, param: float | str, percent: bool = False) -> str:
        if percent:
            param *= 100
        if specifier == "":
            return str(param)
        if specifier.startswith("f"):
            prec = int(specifier[1:])  # may throws ValueError
            return f"{param:.{prec}f}"
        if specifier == "i":
            # TODO: 需要给数字做千分位分隔
            param = round(float(param))
            return str(round(float(param)))
        if specifier == "m":
            # TODO: %1[m] 表示将比如数字 1,000,000 表示成 一百万 等语言对应的缩写形式
            # 仅在罗浮杂俎相关任务和成就中出现，应该暂时用不到
            return str(round(float(param)))
        raise ValueError(f"invalid specifier {specifier}")

    def __flush_format(self, percent: bool = False):
        state = self.__states.pop()
        if state == State.HashSign:
            self.__push("#")
            self.__specifier = ""
            self.__param_num = 0
            return
        if self.__param_num == 0 or len(self.__parameter) == 0 or self.__param_num > len(self.__parameter):
            self.__push("#")
            self.__push(str(self.__param_num))
            if state in (State.Specifier, State.ParamEnd) or self.__specifier != "":
                self.__push("[")
                self.__push(self.__specifier)
            if state != State.Specifier and self.__specifier != "":
                self.__push("]")
            if percent:
                self.__push("%")
            self.__specifier = ""
            self.__param_num = 0
            return
        param = self.__parameter[self.__param_num - 1]
        if state == State.Specifier:  # #1[i 未闭合
            self.__push(str(param))
            self.__push("[")
            self.__push(self.__specifier)
            self.__specifier = ""
            self.__param_num = 0
            return
        try:
            self.__push(self.__do_format(self.__specifier, param, percent))
        except ValueError:  # 两种 ValueError 都是 Specifier 格式错误
            self.__push(str(param))
            self.__push("[")
            self.__push(self.__specifier)
            self.__push("]")
        if percent:
            self.__push("%")
        self.__specifier = ""
        self.__param_num = 0

    def __flush_tag_media_wiki(self, tag: str, val: str, text: str):  # noqa: PLR0912, PLR0915
        if text == "":
            return
        match tag:
            case "align":  # 左中右对齐
                _ = self.__texts[-1].write('<p style="text-align: ')
                match val:
                    case '"center"':
                        _ = self.__texts[-1].write("center")
                    case '"left"':
                        _ = self.__texts[-1].write("lerft")
                    case '"right"':
                        _ = self.__texts[-1].write("right")
                    case _:
                        raise ValueError(f"invalid xml align={repr(val)}")
                _ = self.__texts[-1].write('">')
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("</p>")
                self.__is_inline_block = InlineBlock.Block
            case "b":  # 粗体
                if "<br />" in text:
                    _ = self.__texts[-1].write("<b>")
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("</b>")
                    self.__display_block_afterward()
                    return
                _ = self.__texts[-1].write("'''")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("'''")
                self.__display_block_afterward()
            case "color":
                _ = self.__texts[-1].write("{{颜色|")
                color = ""
                match val:
                    case "#f29e38" | "#f29e3800":
                        color = "描述2"
                    case _:
                        color = val.removeprefix("#")
                _ = self.__texts[-1].write(color)
                _ = self.__texts[-1].write("|")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("}}")
                self.__display_block_afterward()
            case "i" | "I":  # 斜体
                if "<br />" in text:
                    _ = self.__texts[-1].write("<i>")
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("</i>")
                    self.__display_block_afterward()
                    return
                _ = self.__texts[-1].write("''")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("''")
                self.__display_block_afterward()
            case "s":  # 删除线
                _ = self.__texts[-1].write("<s>")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("</s>")
                self.__display_block_afterward()
            case "size":  # 指定字号
                val = val.removesuffix("px")
                px = int(val) + (20 if val.startswith(("+", "-")) else 0)
                em = float(px) / 20.0
                _ = self.__texts[-1].write('<span style="font-size: ')
                _ = self.__texts[-1].write(str(em))
                _ = self.__texts[-1].write('em">')
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("</size>")
                self.__display_block_afterward()
            case "u":  # 下划线
                if (
                    isinstance(self.__game, SRGameData)
                    and text.removeprefix("【").removesuffix("】") in self.__game._extra_effect_config_names  # pyright: ignore[reportPrivateUsage]
                ):
                    _ = self.__texts[-1].write("{{效果说明|")
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("}}")
                else:
                    _ = self.__texts[-1].write("<u>")
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("</u>")
                self.__display_block_afterward()
            case "unbreak":
                _ = self.__texts[-1].write(text)
                self.__display_block_afterward()
            case _:  # unreacheable
                raise ValueError(f"invalid tag {tag}")

    @staticmethod
    def text_width(text: str) -> int:
        """
        这个算法是不精确的，只是为了实现简单才这么写的
        文本宽度计算是老大难问题，和字符类型、终端配置、字体有关
        """
        width = 0
        ignore = False
        for char in text:
            if not ignore and char == "\033":
                ignore = True
            if not ignore:
                if unicodedata.east_asian_width(char) in ("A", "F", "N", "W"):
                    width += 2
                else:
                    width += 1
            if ignore and char == "m":
                ignore = False
        return width

    def __flush_tag_terminal(self, tag: str, val: str, text: str):  # noqa: PLR0912, PLR0915
        """简陋的高亮实现，用来调试输出美观"""
        if text == "":
            return
        match tag:
            case "align":  # 左中右对齐
                self.__is_inline_block = InlineBlock.Block
                if val == '"left"':
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("\n")
                    return
                term = os.get_terminal_size()
                for line in text.splitlines():
                    width = Formatter.text_width(line)
                    if width > term.columns:
                        _ = self.__texts[-1].write(line)
                        _ = self.__texts[-1].write("\n")
                        continue
                    if val == '"center"':
                        padding = (term.columns - width) // 2
                        _ = self.__texts[-1].write(" " * padding)
                        _ = self.__texts[-1].write(line)
                    if val == '"right"':
                        padding = term.columns - width
                        _ = self.__texts[-1].write(" " * padding)
                        _ = self.__texts[-1].write(line)
                    _ = self.__texts[-1].write("\n")
            case "b":  # 粗体
                _ = self.__texts[-1].write(f"\033[1m{text}\033[22m")
                self.__is_inline_block = InlineBlock.Inline
            case "color":
                r = int(val[1:3], 16)
                g = int(val[3:5], 16)
                b = int(val[5:7], 16)
                _ = self.__texts[-1].write(f"\033[38;2;{r};{g};{b}m{text}\033[39m")
                self.__is_inline_block = InlineBlock.Inline
            case "i" | "I":  # 斜体
                _ = self.__texts[-1].write(f"\033[3m{text}\033[23m")
                self.__is_inline_block = InlineBlock.Inline
            case "s":  # 删除线
                _ = self.__texts[-1].write(f"\033[9m{text}\033[29m")
                self.__is_inline_block = InlineBlock.Inline
            case "size":  # 指定字号
                _ = self.__texts[-1].write(text)
                self.__is_inline_block = InlineBlock.Inline
            case "u":  # 下划线
                _ = self.__texts[-1].write(f"\033[4m{text}\033[24m")
                self.__is_inline_block = InlineBlock.Inline
            case "unbreak":
                _ = self.__texts[-1].write(text)
                self.__is_inline_block = InlineBlock.Inline
            case _:  # unreacheable
                raise ValueError(f"invalid tag {tag}")

    @staticmethod
    def __is_known_tag(tag: str) -> bool:
        return tag in {"align", "b", "color", "i", "I", "s", "size", "u", "unbreak"}

    def __flush_tag(self):
        state = self.__states.pop()
        tag = self.__keys.pop().getvalue()
        val = self.__vals.pop().getvalue()
        text = self.__texts.pop().getvalue()
        if state in (State.TagLKey, State.TagLVal):
            self.__push("<")
            self.__push(tag)
            if state == State.TagLVal:
                self.__push("=")
                self.__push(val)
            return
        match self.__syntax:
            case Syntax.Plain:
                self.__push(text)
            case Syntax.MediaWiki | Syntax.MediaWikiPretty:
                self.__flush_tag_media_wiki(tag, val, text)
            case Syntax.Terminal:
                self.__flush_tag_terminal(tag, val, text)

    @staticmethod
    def __is_known_var(var: str) -> bool:
        return var in {"BIRTH", "F", "M", "NICKNAME", "RUBY_B", "RUBY_E", "TEXTJOIN"}

    def __flush_var(self):  # noqa: PLR0912, PLR0915
        _state = self.__states.pop()
        var = self.__keys.pop().getvalue()
        val = self.__vals.pop().getvalue()
        match var:
            case "BIRTH":
                self.__push("生日")
            case "F":  # 一般很短，暂时不考虑堆栈
                if len(self.__m_text) == 0:
                    self.__f_text = val
                    return
                match self.__gender_order:
                    case GenderOrder.Preserve | GenderOrder.Male:
                        self.__push(self.__m_text)
                        self.__push("/")
                        self.__push(val)
                    case GenderOrder.Female:
                        self.__push(val)
                        self.__push("/")
                        self.__push(self.__m_text)
                _ = self.__m_text = ""
            case "M":  # 一般很短，暂时不考虑堆栈
                if len(self.__f_text) == 0:
                    self.__m_text = val
                    return
                match self.__gender_order:
                    case GenderOrder.Preserve | GenderOrder.Female:
                        self.__push(self.__f_text)
                        self.__push("/")
                        self.__push(val)
                    case GenderOrder.Male:
                        self.__push(val)
                        self.__push("/")
                        self.__push(self.__f_text)
                _ = self.__f_text = ""
            case "NICKNAME":
                self.__push("开拓者")  # TODO: 根据游戏区分
            case "RUBY_B":
                if self.__syntax in (Syntax.MediaWiki, Syntax.MediaWikiPretty):
                    self.__push("{{注音|")
                    self.__ruby = val
            case "RUBY_E":
                if self.__syntax in (Syntax.MediaWiki, Syntax.MediaWikiPretty):
                    self.__push("|")
                    self.__push(self.__ruby)
                    _ = self.__ruby = ""
                    self.__push("}}")
            case "TEXTJOIN":
                raise NotImplementedError
            case _:
                raise ValueError(f"invalid var {var}")

    def feed(self, char: str) -> None:  # noqa: PLR0912
        if len(self.__states) == 0:
            self.__feed_text(char)
            return
        match self.__states[-1]:
            case State.HashSign:
                self.__feed_hash_sign(char)
            case State.ParamNum:
                self.__feed_param_num(char)
            case State.Specifier:
                self.__feed_specifier(char)
            case State.ParamEnd:
                self.__feed_param_end(char)
            case State.Escaping:
                self.__feed_escaping(char)
            case State.TagLKey:
                self.__feed_tag_l_key(char)
            case State.TagLVal:
                self.__feed_tag_l_val(char)
            case State.TagText:
                self.__feed_tag_text(char)
            case State.TagRBra:
                self.__feed_tag_r_bra(char)
            case State.TagSlash:
                self.__feed_tag_slash(char)
            case State.VarKey:
                self.__feed_var_key(char)
            case State.VarVal:
                self.__feed_var_val(char)

    def __flush(self) -> None:
        while len(self.__states) != 0:
            match self.__states[-1]:
                case State.HashSign | State.ParamNum | State.Specifier | State.ParamEnd:
                    self.__flush_format()
                case State.Escaping:
                    self.__push("\\")
                    _ = self.__states.pop()
                case State.TagLKey | State.TagLVal | State.TagText | State.TagRBra | State.TagSlash:
                    self.__flush_tag()
                case State.VarKey | State.VarVal:
                    self.__flush_var()

    def format(self, format: str, *args: float | str) -> str:
        self.__parameter = args
        for char in format:
            self.feed(char)
        self.__flush()
        # strip 去除 block 状态带来的最后一个回车
        value = self.__texts[0].getvalue().strip()
        _ = self.__texts[0] = io.StringIO()
        return value
