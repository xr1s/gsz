from __future__ import annotations

import abc
import enum
import functools
import io
import itertools
import typing

from . import model

if typing.TYPE_CHECKING:
    from .. import GameData
    from .sequence import Sequence
    from .task import Task


class WikiStyle(enum.Enum):
    Rogue = 0
    Quest = 1


class Dialogue(abc.ABC):
    _game: GameData

    @functools.cached_property
    @abc.abstractmethod
    def _sequences(self) -> list[Sequence]: ...

    def _find_successors(self, seq: Sequence) -> list[Sequence]:
        """找单个节点在列表中的后继节点"""
        if seq.successors is not None:
            return seq.successors
        if seq.is_leavepoint:
            return []
        if len(seq.trigger_custom_string) != 0:
            # 根据 trigger_custom_string 在整个列表中寻找匹配的 seq
            seq.successors = [
                next_seq
                for next_seq in self._sequences
                if not self._seq_in_search_stack[next_seq.index]
                and next_seq.wait_custom_string in seq.trigger_custom_string
            ]
            return seq.successors
        # 如果没有 trigger_custom_string 就直接返回列表中的下一个
        if seq.index + 1 == len(self._sequences):
            return []
        iter_seq = (seq for seq in self._sequences[seq.index + 1 :] if not seq.is_wait_event and not seq.is_entrypoint)
        next_seq = next(iter_seq, None)
        seq.successors = [] if next_seq is None or self._seq_in_search_stack[next_seq.index] else [next_seq]
        return seq.successors

    @functools.cached_property
    def _seq_in_search_stack(self) -> list[bool]:
        """标记 _find_confluence 深搜过程中的当前搜索路径，避免成环导致无限递归"""
        return [False for _ in self._sequences]

    def _find_confluence(self, seq: Sequence) -> Sequence | None:
        """如果节点是选项节点，找后继汇合的点，否则就是下一个节点"""
        if seq.confluence is not None:
            return seq.confluence
        successors = self._find_successors(seq)
        if len(successors) == 0:
            return None  # 无后继直接退出
        if len(successors) == 1 and not self._seq_in_search_stack[successors[0].index]:
            seq.confluence = successors[0]  # 只有一个后继直接返回
            return seq.confluence
        if not self._seq_in_search_stack[successors[0].index] and all(
            node.index == successors[0].index for node in successors[1:]
        ):
            seq.confluence = successors[0]  # 全等后继直接返回
            return seq.confluence
        # 超绝简化版广搜，因为每个节点只有一个或零个汇聚点，所以队列长度只会减少
        visit: list[int] = [0 for _ in self._sequences]
        for node in successors:
            visit[node.index] = 1
        queue: list[Sequence | None] = list(successors)
        while any(node is not None for node in queue):
            for index, node in enumerate(queue):
                if node is None:
                    continue
                if self._seq_in_search_stack[node.index]:  # 成环，直接退出
                    queue[index] = None
                    continue
                self._seq_in_search_stack[node.index] = True
                next_node = self._find_confluence(node)
                self._seq_in_search_stack[node.index] = False
                queue[index] = next_node
                if next_node is None:
                    continue
                visit[next_node.index] += 1
                if visit[next_node.index] == len(queue) and not self._seq_in_search_stack[next_node.index]:
                    seq.confluence = next_node
                    return seq.confluence
        return None

    def _next_custom_string(self, custom_string: str) -> Sequence | None:
        return next((seq for seq in self._sequences if seq.wait_custom_string == custom_string), None)

    __AEON_NAMES = {
        "阿基维利",
        "纳努克",
        "岚",
        "博识尊",
        "希佩",
        "Ⅸ",
        "克里珀",
        "药师",
        "奥博洛斯",
        "阿哈",
        "浮黎",
        "伊德莉拉",
        "塔伊兹育罗斯",
        "迷思",
        "互",
        "末王",
        "太一",
        "龙",
    }

    @property
    def _formatter(self):
        return self._game._mw_formatter  # pyright: ignore[reportPrivateUsage]

    @property
    def _pretty_formatter(self):
        return self._game._mw_pretty_formatter  # pyright: ignore[reportPrivateUsage]

    def _write_simple(self, style: WikiStyle, wiki: io.StringIO, indent: str, task: Task):
        backgrounds = list(task.backgrounds())
        for index, talk in enumerate(task.talks()):
            if index < len(backgrounds) and backgrounds[index] is not None:
                _ = wiki.write(indent)
                _ = wiki.write(f"<!-- 背景: {backgrounds[index]} -->")
            match style:
                case WikiStyle.Rogue:
                    _ = wiki.write(indent)
                    _ = wiki.write("{{事件|")
                    name = self._formatter.format(talk.name)
                    if task.is_(model.task.PlayAeonTalk) or name in self.__AEON_NAMES:
                        _ = wiki.write("星神|")
                    _ = wiki.write(name)
                    _ = wiki.write("|")
                    _ = wiki.write(self._formatter.format(talk.text))
                    _ = wiki.write("}}")
                case WikiStyle.Quest:
                    _ = wiki.write("\n")
                    if talk.name != "":
                        _ = wiki.write("* ")
                        name = self._formatter.format(talk.name)
                        _ = wiki.write(name)
                        _ = wiki.write("：")
                    else:
                        _ = wiki.write(": ")
                    _ = wiki.write(self._formatter.format(talk.text))

    def _write_dialogue_option_no_wrap(
        self,
        style: WikiStyle,
        wiki: io.StringIO,
        indent: str,
        options: list[model.talk.OptionTalk],
        confluence: Sequence | None,
    ):
        for index, option in enumerate(options):
            number = index + 1
            _ = wiki.write(f"|选项{number}=")
            if option.talk_sentence_id is not None:
                talk = self._game.talk_sentence_config(option.talk_sentence_id)
                _ = wiki.write("" if talk is None else self._formatter.format(talk.text))
            else:
                assert option.option_textmap_id is not None
                _ = wiki.write(self._formatter.format(self._game.text(option.option_textmap_id)))
            if option.option_icon_type not in (None, model.talk.OptionIconType.ChatContinueIcon):
                _ = wiki.write(f"|图标{number}={option.option_icon_type.wiki()}")
        _ = wiki.write("}}")
        if options[0].trigger_custom_string is not None:
            next_seq = self._next_custom_string(options[0].trigger_custom_string)
            if next_seq is not None:
                self._wiki_iter_seq(style, wiki, indent, next_seq, confluence)

    def _write_dialogue_option(
        self,
        style: WikiStyle,
        wiki: io.StringIO,
        indent: str,
        options: list[model.talk.OptionTalk],
        confluence: Sequence | None,
    ):
        _ = wiki.write(indent)
        _ = wiki.write("{{剧情选项")
        if all(option.trigger_custom_string == options[0].trigger_custom_string for option in options[1:]):
            # 选项的后继全部相同，所有选项压成一行即可
            self._write_dialogue_option_no_wrap(style, wiki, indent, options, confluence)
            return
        for index, option in enumerate(options):
            number = index + 1
            _ = wiki.write(indent)
            _ = wiki.write(f"|选项{number}=")
            if option.talk_sentence_id is not None:
                talk = self._game.talk_sentence_config(option.talk_sentence_id)
                _ = wiki.write("" if talk is None else self._formatter.format(talk.text))
            else:
                assert option.option_textmap_id is not None
                _ = wiki.write(self._formatter.format(self._game.text(option.option_textmap_id)))
            if option.option_icon_type not in (None, model.talk.OptionIconType.ChatContinueIcon):
                _ = wiki.write(indent)
                _ = wiki.write(f"|图标{number}={option.option_icon_type.wiki()}")
            if option.trigger_custom_string is None or option.trigger_custom_string == "":
                continue
            seq = self._next_custom_string(option.trigger_custom_string)
            if (
                seq is None  # 无后继节点跳出
                or self._seq_in_search_stack[seq.index]  # 后继节点已经深搜过了（成环）跳出
                or (confluence is not None and seq.index == confluence.index)  # 后继节点是汇聚节点跳出
            ):
                continue
            _ = wiki.write(indent)
            _ = wiki.write(f"|剧情{number}=")
            self._seq_in_search_stack[seq.index] = True
            self._wiki_iter_seq(style, wiki, indent + "  ", seq, confluence)
            self._seq_in_search_stack[seq.index] = False
        _ = wiki.write(indent)
        _ = wiki.write("}}")

    def _write_option(self, style: WikiStyle, wiki: io.StringIO, indent: str, task: Task, confluence: Sequence | None):
        options = list(task.options())
        if len(options) == 0:
            return
        self._write_dialogue_option(style, wiki, indent, options, confluence)

    def _write_predicate(self, style: WikiStyle, wiki: io.StringIO, indent: str, seq: Sequence, task: Task):
        from .task import Task

        _task = task._task  # pyright: ignore[reportPrivateUsage]
        assert isinstance(_task, model.task.PredicateTaskList)
        if _task.success_task_list is None and _task.failed_task_list is None:
            return
        if _task.success_task_list is None or _task.failed_task_list is None:
            for next_task in itertools.chain(_task.success_task_list or (), _task.failed_task_list or ()):
                self.__do_task(style, wiki, indent, seq, Task(self._game, next_task))
            return
        success, failure = task.predicate_titles()
        _ = wiki.write(indent)
        _ = wiki.write("{{切换板|开始}}")
        _ = wiki.write(indent)
        _ = wiki.write(f"  {{{{切换板|默认显示|{success}}}}}")
        _ = wiki.write(indent)
        _ = wiki.write(f"  {{{{切换板|默认折叠|{failure}}}}}")
        _ = wiki.write(indent)
        _ = wiki.write("  {{切换板|显示内容}}")
        for success in _task.success_task_list:
            self.__do_task(style, wiki, indent + "    ", seq, Task(self._game, success))
        _ = wiki.write(indent)
        _ = wiki.write("  {{切换板|内容结束}}")
        _ = wiki.write(indent)
        _ = wiki.write("  {{切换板|折叠内容}}")
        for failure in _task.failed_task_list:
            self.__do_task(style, wiki, indent + "    ", seq, Task(self._game, failure))
        _ = wiki.write(indent)
        _ = wiki.write("  {{切换板|内容结束}}")
        _ = wiki.write(indent)
        _ = wiki.write("{{切换板|结束}}")

    def __do_task(self, style: WikiStyle, wiki: io.StringIO, indent: str, seq: Sequence, task: Task):  # noqa: PLR0912
        _task = task._task  # pyright: ignore[reportPrivateUsage]
        if task.is_skip:
            pass  # 故意用 pass，否则 linter 会提示下面 elif 不需要，但是改掉的话后面就不对称了
        elif task.is_simple:
            self._write_simple(style, wiki, indent, task)
        elif task.is_option:
            next_confluence = self._find_confluence(seq)
            self._write_option(style, wiki, indent, task, next_confluence)
        elif task.is_(model.task.PredicateTaskList):
            self._write_predicate(style, wiki, indent, seq, task)
        elif task.is_(model.task.PlayMessage):
            # 剧情中收到短信
            assert isinstance(_task, model.task.PlayMessage)
            section = self._game.message_section_config(_task.message_section_id)
            if section is not None:
                _ = wiki.write("\n")
                _ = wiki.write(section.wiki())
        elif isinstance(_task, model.task.ShowReading):
            # 剧情中打开阅读物
            book = self._game.localbook_config(_task.book_id.fixed_value.value)
            assert book is not None
            _ = wiki.write("\n{{折叠|开始|标题=")
            _ = wiki.write(self._formatter.format(book.name))
            _ = wiki.write("|折叠=是}}\n")
            _ = wiki.write(self._pretty_formatter.format(book.content))
            _ = wiki.write("\n{{折叠|结束}}\n")
        elif isinstance(_task, model.task.TalkFigure):
            # 剧情中弹出图片
            _ = wiki.write(f"{indent}<gallary><!-- {_task.image_path} --></gallary>")
        elif isinstance(_task, model.task.PerformanceTransition | model.task.PlayScreenTransfer):
            # 转场，TextEnabled 时，黑屏时出现居中的文案
            if not _task.text_enabled or _task.talk_sentence_id is None:
                return
            talk = self._game.talk_sentence_config(_task.talk_sentence_id)
            if talk is None:
                return
            _ = wiki.write(indent if style is WikiStyle.Rogue else "\n: ")
            _ = wiki.write("{{颜色|描述|")
            _ = wiki.write(self._formatter.format(talk.text))
            _ = wiki.write("}}")
        elif task.is_(model.task.WaitDialogueEvent):
            # TODO: 很重要，但是没搞懂机制
            # 感觉是先随机在几个 SuccessCustomString 里随机选一个，然后开始后续剧情
            pass
        else:
            raise ValueError(f"unknown task type {task._task.typ}")  # pyright: ignore[reportPrivateUsage]

    def _wiki_iter_seq(
        self, style: WikiStyle, wiki: io.StringIO, indent: str, seq: Sequence, confluence: Sequence | None
    ):
        if confluence is not None and seq.index == confluence.index:
            return
        for task in seq.tasks():
            self.__do_task(style, wiki, indent, seq, task)
        next_seq = self._find_confluence(seq)
        if next_seq is not None and not self._seq_in_search_stack[next_seq.index]:
            self._seq_in_search_stack[next_seq.index] = True
            self._wiki_iter_seq(style, wiki, indent, next_seq, confluence)
            self._seq_in_search_stack[next_seq.index] = False

    def __wiki_debug(self):  # noqa: PLR0912
        for seq in self._sequences:
            self._seq_in_search_stack[seq.index] = True
            if not seq.is_entrypoint and not seq.is_leavepoint and not seq.is_wait_event:
                print(" ", end="")
            elif seq.is_entrypoint:
                print(">", end="")  # 进入
            elif seq.is_leavepoint:
                print("<", end="")  # 退出
            elif seq.is_wait_event:
                print("=", end="")  # 等待
            print(seq.index)
            if seq.wait_custom_string != "":
                print(f"    条件 [{repr(seq.wait_custom_string)}]")
            print(f"    触发 {seq.trigger_custom_string}")
            print(f"    后继 {[seq.index for seq in self._find_successors(seq)]}", end="")
            confluence = self._find_confluence(seq)
            if confluence is not None:
                print(f" 汇聚 {confluence.index}", end="")
            print()
            for task in seq.tasks():
                for talk in task.talks():
                    print("   ", f"{{{{事件|{talk.name}|{talk.text}}}}}")
                for option in task.options():
                    assert isinstance(option, model.talk.OptionTalkInfo)
                    assert option.talk_sentence_id is not None
                    talk = self._game.talk_sentence_config(option.talk_sentence_id)
                    assert talk is not None
                    print("   ", f"{talk.name}| {talk.text}")
                if task.is_(model.task.TriggerCustomString | model.task.TriggerCustomStringOnDialogEnd):
                    next_seq = self._next_custom_string(task.trigger_custom_string)
                    if next_seq is not None:
                        print(f"    \033[4;38;2;255;255;0mgoto {next_seq.index}\033[39;24m")
                act_task = task._task  # pyright: ignore[reportPrivateUsage]
                if isinstance(act_task, model.task.TriggerDialogueEvent):
                    print("    trigger dialogue event", act_task.dialogue_event_id)
            self._seq_in_search_stack[seq.index] = False

    def wiki(self, *, debug: bool = False, style: WikiStyle = WikiStyle.Rogue) -> str:
        if len(self._sequences) == 0:
            return ""
        if debug:
            self.__wiki_debug()
        wiki = io.StringIO()
        entrypoint = next(seq for seq in self._sequences if seq.is_entrypoint)
        self._seq_in_search_stack[entrypoint.index] = True
        indent = "\n  " if style is WikiStyle.Rogue else "\n"
        self._wiki_iter_seq(style, wiki, indent, entrypoint, None)
        self._seq_in_search_stack[entrypoint.index] = False
        return wiki.getvalue()
