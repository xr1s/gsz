from __future__ import annotations

import collections.abc
import enum
import functools
import html
import io
import os
import typing
import unicodedata

if typing.TYPE_CHECKING:
    from . import SRGameData, ZZZGameData


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
    * Unity Rich Text，类似 XML 的 DSL，有以下形式 <u> </i> <color=#0000> <size=20> <size=+2>
    * 某种特殊的变量 DSL，有以下形式
        {BIRTH}
        {F#女性主角分支} {M#男性主角分支}
        {RUBY_B#注音内容}对话内容{RUBY_E}
        {TEXTJOIN#编号}
    """

    HashSign = 10
    """HashSign 表示格式化字符串中的第一个井号字符，表示后面有格式化字符串内容"""
    ParamNum = 11
    """ParamNum 表示格式化字符串井号和左方括号中间的数字，指引用参数列表中的第几个参数"""
    Specifier = 12
    """
    Specifier 表示方括号之间的格式化串，可能为
    * 空（不会进入本状态）
    * f 后接一个数字，表示保留多少位小数的浮点数
    * i 表示整数，可能有千位分隔符
    * m 表示将数字 1,000,000 表示成「一百万」等，各语言对应的缩写形式
    """
    ParamEnd = 13
    """ParamEnd 表示格式化字符串中的右方括号，需要再读一个字符决定后续走向 Percent 还是 Literal"""
    Escaping = 14
    """目前只有 \\n 这一个需要转义的"""
    TagLKey = 20
    """TagLKey 表示类 XML 标识中的标签名，比如 <u> </i> <size=20>，中的 u i size"""
    TagLVal = 21
    """TagLVal 表示类 XML 标识比如 <color=#000000> <size=20> 中的 #000000 20"""
    TagText = 22
    """TagText 表示标签内部的正文"""
    TagRBra = 23
    """
    TagRBra 表示 TagText 中间出现的 <

    注意可能是嵌套的 Tag，比如 <align="right"><i>这里是正文</i></align>
    所以后续可能转移到下一个 TagLVal 中
    """
    TagSlash = 24
    """
    XML Tag 形式的标识，可能有以下标签 <u> <i> <color=#000000> <size=20> <size=+2>
    TagSlash 表示 </i> 的 /
    """
    VarKey = 30
    """VarKey 记录比如 {BIRTH} <RUBY_B#注音内容> 中的 BIRTH RUBY_B"""
    VarVal = 31
    """VarKey 记录比如 {F#女性主角分支} {RUBY_B#注音内容} 中的 女性主角分支 注音内容"""
    AnsiEscape = 40
    """删除多余的 AnsiSeq"""


class InlineBlock(enum.Enum):
    Inline = False
    Block = True


class Formatter:
    def __init__(
        self,
        *,
        syntax: Syntax | None = None,
        game: SRGameData | ZZZGameData | None = None,
        gender_order: GenderOrder = GenderOrder.Preserve,
        percent_as_plain: bool = False,
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
        self.__percent_as_plain: bool = percent_as_plain
        # var 相关状态
        self.__gender_order = gender_order
        self.__f_text = ""
        self.__m_text = ""
        self.__ruby = ""
        self.__localbook_img: list[str] | None = None

    def __push(self, s: str):
        match self.__syntax:
            case Syntax.Plain:
                _ = self.__texts[-1].write(s)
            case Syntax.Terminal:
                for char in s:
                    _ = self.__texts[-1].write(char)
                    if char in "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯ":
                        _ = self.__texts[-1].write(" ")
            case Syntax.MediaWiki | Syntax.MediaWikiPretty:
                for char in s:
                    match char:
                        case " " | "\xa0":
                            _ = self.__texts[-1].write("&nbsp;")
                        case "\n":
                            _ = self.__texts[-1].write("<br />")
                        case "=":
                            _ = self.__texts[-1].write("{{=}}")
                        case "|":
                            _ = self.__texts[-1].write("&#x7c;")
                        case _:
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
            case "\x1b" if self.__syntax == Syntax.Plain:
                self.__states.append(State.AnsiEscape)
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
        if not self.__percent_as_plain and char == "%":
            return self.__flush_format(True)
        self.__flush_format()
        return self.__feed(char)

    def __feed_specifier(self, char: str) -> None:
        if char == "]":
            self.__states[-1] = State.ParamEnd
            return
        self.__specifier += char

    def __feed_param_end(self, char: str) -> None:
        if not self.__percent_as_plain and char == "%":
            self.__flush_format(True)
            return
        self.__flush_format()
        self.__feed(char)

    def __feed_escaping(self, char: str) -> None:
        _ = self.__states.pop()
        if char == "n":
            if self.__is_inline_block == InlineBlock.Block:
                self.__is_inline_block = InlineBlock.Inline
                if self.__syntax == Syntax.MediaWikiPretty:
                    _ = self.__texts[-1].write("\n")
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
        if char == "<":
            # 有 <<<</align> 这种特殊情况
            # 说明前序也是 <，直接 push 没问题
            self.__push("<")
            return
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

    def __feed_ansi_seq(self, char: str) -> None:
        if char == "m":
            _ = self.__states.pop()

    @staticmethod
    def __do_format(specifier: str, param: float | str, percent: bool = False) -> str:
        if percent:
            param *= 100
        if specifier == "":
            match param:
                case int():
                    return str(param)
                case float():
                    return str(int(param)) if param.is_integer() else str(param).rstrip("0").rstrip(".")
                case str():
                    return param
        if specifier.startswith("f"):
            prec = int(specifier[1:])  # may throws ValueError
            return f"{param:.{prec}f}"
        if specifier == "i":
            param = round(float(param))
            return f"{round(float(param)):,}"
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
        from . import SRGameData

        if text == "":
            return
        match tag:
            case "align":  # 左中右对齐
                if val == '"left"':
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("<br />")
                    return
                _ = self.__texts[-1].write('<p style="text-align: ')
                match val:
                    case '"center"':
                        _ = self.__texts[-1].write("center")
                    case '"right"':
                        _ = self.__texts[-1].write("right")
                    case _:
                        raise ValueError(f"invalid xml align={val!r}")
                _ = self.__texts[-1].write('">')
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("</p>")
                self.__is_inline_block = InlineBlock.Block
            case "b":  # 粗体
                if "<br />" in text:
                    _ = self.__texts[-1].write("<b>")
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("</b>")
                    return
                _ = self.__texts[-1].write("'''")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("'''")
            case "color":
                _ = self.__texts[-1].write("{{颜色|")
                color = ""
                match val:
                    case "#f29e38" | "#f29e38ff":
                        color = "描述2"
                    case _:
                        color = val.removeprefix("#")
                _ = self.__texts[-1].write(color)
                _ = self.__texts[-1].write("|")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("}}")
            case "i" | "I":  # 斜体
                if "<br />" in text:
                    _ = self.__texts[-1].write("<i>")
                    _ = self.__texts[-1].write(text)
                    _ = self.__texts[-1].write("</i>")
                    return
                _ = self.__texts[-1].write("''")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("''")
            case "s":  # 删除线
                _ = self.__texts[-1].write("<s>")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("</s>")
            case "size":  # 指定字号
                val = val.removesuffix("px")
                px = int(val) + (20 if val.startswith(("+", "-")) else 0)
                em = float(px) / 20.0
                _ = self.__texts[-1].write('<span style="font-size: ')
                _ = self.__texts[-1].write(str(round(em, 2)).rstrip("0").rstrip("."))
                _ = self.__texts[-1].write('em">')
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("</span>")
            case "u":  # 下划线
                has_quote = text.startswith("【") and text.endswith("】")
                without_quote = text.removeprefix("【").removesuffix("】")
                if (
                    isinstance(self.__game, SRGameData) and without_quote in self.__game._extra_effect_config_names  # pyright: ignore[reportPrivateUsage]
                ):
                    if has_quote:
                        _ = self.__texts[-1].write("【")
                    _ = self.__texts[-1].write("{{效果说明|")
                    _ = self.__texts[-1].write(without_quote)
                    _ = self.__texts[-1].write("}}")
                    if has_quote:
                        _ = self.__texts[-1].write("】")
                    return
                _ = self.__texts[-1].write("<u>")
                _ = self.__texts[-1].write(text)
                _ = self.__texts[-1].write("</u>")
            case "unbreak":
                _ = self.__texts[-1].write(text)
            case _:  # unreacheable
                raise ValueError(f"invalid tag {tag}")

    @functools.cache
    @staticmethod
    def __plain_formatter():
        return Formatter()

    @staticmethod
    def text_width(text: str) -> int:
        """
        这个算法是不完全精确的，只是为了实现简单才这么写的
        文本宽度计算是老大难问题，和字符类型、终端配置、字体有关
        """
        text = Formatter.__plain_formatter().format(text)
        return sum(
            2 if unicodedata.east_asian_width(char) in "AFNW" or char in "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯ" else 1 for char in text
        )

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
        return var in {"BIRTH", "F", "Img", "M", "NICKNAME", "RUBY_B", "RUBY_E", "TEXTJOIN"}

    @functools.cached_property
    def __text_join_item_formatter(self):
        return Formatter(syntax=self.__syntax, game=self.__game, gender_order=self.__gender_order)

    def __flush_var(self):  # noqa: PLR0911, PLR0912, PLR0915
        from . import SRGameData, ZZZGameData

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
            case "Img":
                if self.__localbook_img is None:
                    _ = self.__texts[-1].write("{{Img#")
                    self.__push(f"{val}")
                    return
                index = int(val)
                if index > len(self.__localbook_img):
                    _ = self.__texts[-1].write("{{Img#")
                    self.__push(f"{val}")
                    return
                _ = self.__texts[-1].write(f"<!-- {self.__localbook_img[index - 1]} -->")
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
                match self.__game:
                    case SRGameData():
                        self.__push("开拓者")
                    case ZZZGameData():
                        self.__push("绳匠")
                    case None:
                        self.__push("主角")
            case "RUBY_B":
                if self.__syntax in (Syntax.MediaWiki, Syntax.MediaWikiPretty):
                    _ = self.__texts[-1].write("{{注音|")
                    self.__ruby = val
            case "RUBY_E":
                if self.__syntax in (Syntax.MediaWiki, Syntax.MediaWikiPretty):
                    _ = self.__texts[-1].write("|")
                    self.__push(self.__ruby)
                    _ = self.__ruby = ""
                    _ = self.__texts[-1].write("}}")
            case "TEXTJOIN":
                if not isinstance(self.__game, SRGameData):
                    self.__push(f"{{TEXTJOIN#{val}}}")
                    return
                (default, items) = self.__game._text_join_config_item(int(val))  # pyright: ignore[reportPrivateUsage]
                if len(items) == 0:
                    return
                if len(items) <= default:
                    default = 0
                if self.__syntax in (Syntax.Plain, Syntax.Terminal):
                    _ = self.__texts[-1].write("/".join(self.__text_join_item_formatter.format(item) for item in items))
                    return
                if self.__syntax == Syntax.MediaWiki or (
                    self.__syntax == Syntax.MediaWikiPretty
                    and all(self.text_width(item) < 20 for item in items)
                    and sum(len(item) for item in items) < 100
                ):
                    if default != 0:
                        _ = self.__texts[-1].write("{{黑幕|")
                        _ = self.__texts[-1].write(
                            "/".join(self.__text_join_item_formatter.format(item) for item in items[:default])
                        )
                        _ = self.__texts[-1].write("/}}")
                    _ = self.__texts[-1].write(self.__text_join_item_formatter.format(items[default]))
                    if default != len(items) - 1:
                        _ = self.__texts[-1].write("{{黑幕|/")
                        _ = self.__texts[-1].write(
                            "/".join(self.__text_join_item_formatter.format(item) for item in items[default + 1 :])
                        )
                        _ = self.__texts[-1].write("}}")
                    return
                if self.__syntax == Syntax.MediaWikiPretty:
                    self.__display_block_afterward()
                    _ = self.__texts[-1].write("{{切换板|开始}}")
                    for index in range(len(items)):
                        _ = self.__texts[-1].write(
                            "\n  {{切换板|默认" + ("显示" if index == default else "折叠") + "|<!-- 补充标题 -->}}"
                        )
                    for index, item in enumerate(items):
                        _ = self.__texts[-1].write("\n  ")
                        _ = self.__texts[-1].write("{{切换板|" + ("显示" if index == default else "折叠") + "内容}}")
                        _ = self.__texts[-1].write(self.__text_join_item_formatter.format(item))
                        _ = self.__texts[-1].write("{{切换板|内容结束}}")
                    _ = self.__texts[-1].write("\n{{切换板|结束}}")
            case _:
                raise ValueError(f"invalid var {var}")

    def __feed(self, char: str) -> None:  # noqa: PLR0912
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
            case State.AnsiEscape:
                self.__feed_ansi_seq(char)

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
                case State.AnsiEscape:
                    _ = self.__states.pop()

    def format(
        self,
        format: str,
        argument: float | str | tuple[float | str, ...] | collections.abc.Sequence[float | str] = (),
        /,
        *args: float | str,
        image_path: list[str] | None = None,
    ) -> str:
        if isinstance(argument, tuple | collections.abc.Sequence):
            self.__parameter = tuple(argument)
        else:
            self.__parameter = (argument,) + args
        if image_path is not None:
            self.__localbook_img = image_path
        else:
            self.__localbook_img = None
        for char in format:
            self.__feed(char)
        self.__is_inline_block = InlineBlock.Inline
        self.__flush()
        value = self.__texts[0].getvalue().rstrip("\n")
        _ = self.__texts[0] = io.StringIO()
        return value
