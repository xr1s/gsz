from __future__ import annotations
import functools
import io
import typing

from .. import act

if typing.TYPE_CHECKING:
    import collections.abc
    import pathlib
    import types

    from ..data import GameData
    from .rogue import RogueDialogueDynamicDisplay, RogueDialogueOptionDisplay, RogueEventSpecialOption
    from .talk import TalkSentenceConfig


class Act:
    def __init__(self, game: GameData, excel: pathlib.Path | act.Act):
        self._game: GameData = game
        self._act: act.Act = (
            excel if isinstance(excel, act.Act) else act.Act.model_validate_json(game.base.joinpath(excel).read_bytes())
        )

    @functools.cached_property
    def __tasks(self) -> list[act.Task]:
        return (
            []
            if self._act.on_start_sequece is None
            else [task for seq in self._act.on_start_sequece for task in seq.task_list]
        )

    def tasks(self) -> collections.abc.Iterable[Task]:
        return (Task(self._game, task) for task in self.__tasks)

    def on_start_sequence(self) -> collections.abc.Iterable[Sequence]:
        if self._act.on_start_sequece is None:
            return ()
        return (Sequence(self._game, seq, index) for index, seq in enumerate(self._act.on_start_sequece))


class Sequence:
    def __init__(self, game: GameData, excel: act.Sequence, index: int):
        self._game: GameData = game
        self._seq: act.Sequence = excel
        self.successors: list[Sequence] | None = None
        self.confluence: Sequence | None = None
        self.index: int = index

    def tasks(self) -> collections.abc.Iterable[Task]:
        return (Task(self._game, task) for task in self._seq.task_list)

    @functools.cached_property
    def wait_custom_string(self) -> str:
        for task in self._seq.task_list:
            if isinstance(task, act.task.WaitCustomString):
                return task.custom_string.value
        return ""

    @functools.cached_property
    def trigger_custom_string(self) -> list[str]:
        for task in self._seq.task_list:
            if isinstance(task, act.task.TriggerCustomString):
                return [task.custom_string.value]
            if isinstance(task, act.task.PlayRogueOptionTalk):
                return [
                    option.trigger_custom_string
                    for option in task.option_list
                    if option.trigger_custom_string is not None
                ]
            if isinstance(task, act.task.WaitDialogueEvent):
                return [
                    typing.cast(str, event.success_custom_string or event.failure_custom_string)
                    for event in task.dialogue_event_list
                ]
        return []

    @functools.cached_property
    def is_entrypoint(self) -> bool:
        return any(isinstance(task, act.task.ShowRogueTalkUI) for task in self._seq.task_list)

    @functools.cached_property
    def is_leavepoint(self) -> bool:
        return any(isinstance(task, act.task.WaitPerformanceEnd) for task in self._seq.task_list)

    @functools.cached_property
    def is_wait_event(self) -> bool:
        return any(
            isinstance(task, act.task.WaitCustomString | act.task.WaitDialogueEvent) for task in self._seq.task_list
        )


class Task:
    def __init__(self, game: GameData, excel: act.Task):
        self._game: GameData = game
        self._task: act.Task = excel

    def is_(self, typ: type | types.UnionType) -> bool:
        return isinstance(self._task, typ)

    @property
    def trigger_custom_string(self) -> str:
        if isinstance(self._task, act.task.TriggerCustomString):
            return self._task.custom_string.value
        return ""

    @property
    def wait_custom_string(self) -> str:
        if isinstance(self._task, act.task.WaitCustomString):
            return self._task.custom_string.value
        return ""

    @functools.cached_property
    def __talks(self) -> list[TalkSentenceConfig]:
        if isinstance(
            self._task,
            act.task.PlayAeonTalk  # 游戏中会连续弹出许多概念作为名字
            | act.task.PlayRogueSimpleTalk
            | act.task.PlayAndWaitRogueSimpleTalk
            | act.task.PlayAeonTalk,
        ):
            return list(self._game.talk_sentence_config(talk.talk_sentence_id for talk in self._task.simple_talk_list))
        return []

    def talks(self) -> collections.abc.Iterable[TalkSentenceConfig]:
        from .talk import TalkSentenceConfig

        return (TalkSentenceConfig(self._game, talk._excel) for talk in self.__talks)  # pyright: ignore[reportPrivateUsage]

    @functools.cached_property
    def __rogue_options(self) -> list[act.talk.RogueOptionTalk]:
        if isinstance(self._task, act.task.PlayRogueOptionTalk):
            return self._task.option_list
        return []

    def rogue_options(self) -> collections.abc.Iterable[act.talk.RogueOptionTalk]:
        return (option for option in self.__rogue_options)


class Option:
    def __init__(
        self,
        game: GameData,
        option_id: int,
        option: RogueDialogueOptionDisplay,
        special: RogueEventSpecialOption | None,
        dynamic: list[RogueDialogueDynamicDisplay],
        desc_value: list[int | str],
    ):
        self._game: GameData = game
        self.__id = option_id
        self.__option = option
        self.__special = special
        self.__dynamic = dynamic
        self.__desc_value = desc_value

    @property
    def id(self) -> int:
        return self.__id

    @property
    def option(self) -> RogueDialogueOptionDisplay:
        from .rogue import RogueDialogueOptionDisplay

        return RogueDialogueOptionDisplay(self._game, self.__option._excel)  # pyright: ignore[reportPrivateUsage]

    @property
    def special(self) -> RogueEventSpecialOption | None:
        if self.__special is None:
            return None
        from .rogue import RogueEventSpecialOption

        return RogueEventSpecialOption(self._game, self.__special._excel)  # pyright: ignore[reportPrivateUsage]

    @property
    def dynamic(self) -> list[RogueDialogueDynamicDisplay]:
        from .rogue import RogueDialogueDynamicDisplay

        return [RogueDialogueDynamicDisplay(self._game, dynamic._excel) for dynamic in self.__dynamic]  # pyright: ignore[reportPrivateUsage]

    @property
    def desc_value(self) -> list[int | str]:
        return self.__desc_value


class Dialogue:
    def __init__(self, game: GameData, excel: act.Dialogue):
        self._game: GameData = game
        self._dialogue: act.Dialogue = excel

    @property
    def progress(self) -> int | None:
        return self._dialogue.dialogue_progress

    @functools.cached_property
    def dialogue_path(self) -> pathlib.Path:
        return self._game.base / self._dialogue.dialogue_path.strip()

    @functools.cached_property
    def __dialogue(self) -> act.Act:
        return act.Act.model_validate_json(self.dialogue_path.read_bytes())

    def dialogue(self) -> Act:
        return Act(self._game, self.__dialogue)

    @functools.cached_property
    def option_path(self) -> pathlib.Path | None:
        return None if self._dialogue.option_path is None else self._game.base / self._dialogue.option_path.strip()

    @functools.cached_property
    def __opt(self) -> act.Opt | None:
        if self.option_path is None:
            return None
        return act.Opt.model_validate_json(self.option_path.read_bytes())

    @functools.cached_property
    def __options(self) -> list[Option]:
        if self.__opt is None:
            return []
        options: list[Option] = []
        for opt in self.__opt.option_list:
            option = self._game.rogue_dialogue_option_display(opt.display_id)
            assert option is not None
            special = (
                None if opt.special_option_id is None else self._game.rogue_event_special_option(opt.special_option_id)
            )
            desc_value: list[int | str] = []
            dynamic: list[RogueDialogueDynamicDisplay] = []
            if opt.dynamic_map is not None and len(opt.dynamic_map) != 0:
                dynamic_ids = [dynamic.display_id for dynamic in opt.dynamic_map.values()]
                dynamic = list(self._game.rogue_dialogue_dynamic_display(dynamic_ids))
                desc_value.append("、".join(dyn.content for dyn in dynamic))
            if opt.desc_value is not None:
                if len(desc_value) != 1:  # desc_value 传入作为 #2
                    desc_value.append("")
                desc_value.append(opt.desc_value)
            if opt.desc_value2 is not None:
                while len(desc_value) < 4:  # desc_value2 传入作为 #5
                    desc_value.append("")
                desc_value.append(opt.desc_value2)
            if opt.desc_value3 is not None:
                while len(desc_value) < 5:  # desc_value3 传入作为 #6
                    desc_value.append("")
                desc_value.append(opt.desc_value3)
            if opt.desc_value4 is not None:
                while len(desc_value) < 6:  # desc_value4 传入作为 #7
                    desc_value.append("")
                desc_value.append(opt.desc_value4)
            options.append(Option(self._game, opt.option_id, option, special, dynamic, desc_value))
        return options

    @functools.cached_property
    def __option_dict(self) -> dict[int, Option]:
        return {option.id: option for option in self.__options}

    def option(self) -> collections.abc.Iterable[Option]:
        return (
            Option(self._game, option.id, option.option, option.special, list(option.dynamic), option.desc_value)
            for option in self.__options
        )

    @functools.cached_property
    def __sequences(self) -> list[Sequence]:
        if self.__dialogue.on_start_sequece is None:
            return []
        return [Sequence(self._game, seq, index) for index, seq in enumerate(self.__dialogue.on_start_sequece)]

    @functools.cached_property
    def __formatter(self):
        from ...format import Formatter, Syntax

        return Formatter(syntax=Syntax.MediaWiki, game=self._game, percent_as_plain=True)

    def __find_successors(self, seq: Sequence) -> list[Sequence]:
        """找单个节点在列表中的后继节点"""
        if seq.successors is not None:
            return seq.successors
        if seq.is_leavepoint:
            return []
        if len(seq.trigger_custom_string) == 0:
            # 如果没有 trigger_custom_string 就直接返回列表中的下一个
            if seq.index + 1 == len(self.__sequences):
                return []
            iter_seq = (
                seq for seq in self.__sequences[seq.index + 1 :] if not seq.is_wait_event and not seq.is_entrypoint
            )
            next_seq = next(iter_seq, None)
            seq.successors = [] if next_seq is None else [next_seq]
        else:
            # 否则根据 trigger_custom_string 在整个列表中寻找匹配的 seq
            seq.successors = [
                sequence for sequence in self.__sequences if sequence.wait_custom_string in seq.trigger_custom_string
            ]
        return seq.successors

    def __find_confluence(self, seq: Sequence) -> Sequence | None:
        """如果节点是选项节点，找后继汇合的点，否则就是下一个节点"""
        if seq.confluence is not None:
            return seq.confluence
        successors = self.__find_successors(seq)
        if len(successors) == 0:
            return None  # 无后继直接退出
        if len(successors) == 1:
            seq.confluence = successors[0]  # 只有一个后继直接返回
            return seq.confluence
        if all(node.index == successors[0].index for node in successors[1:]):
            seq.confluence = successors[0]  # 全等后继直接返回
            return seq.confluence
        visit: list[int] = [0 for _ in self.__sequences]
        for node in successors:
            visit[node.index] = 1
        queue: list[Sequence | None] = list(successors)
        while any(node is not None for node in queue):
            for index, node in enumerate(queue):
                if node is None:
                    continue
                next_node = self.__find_confluence(node)
                queue[index] = next_node
                if next_node is None:
                    continue
                visit[next_node.index] += 1
                if visit[next_node.index] == len(queue):
                    seq.confluence = next_node
                    return seq.confluence
        return None

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

    def __write_simple(self, wiki: io.StringIO, indent: str, task: Task):
        for talk in task.talks():
            _ = wiki.write(indent)
            _ = wiki.write("{{事件|")
            name = self.__formatter.format(talk.name)
            if task.is_(act.task.PlayAeonTalk) or name in self.__AEON_NAMES:
                _ = wiki.write("星神|")
            _ = wiki.write(name)
            _ = wiki.write("|")
            _ = wiki.write(self.__formatter.format(talk.text))
            _ = wiki.write("}}")

    def __next_custom_string(self, custom_string: str) -> Sequence | None:
        return next((seq for seq in self.__sequences if seq.wait_custom_string == custom_string), None)

    def __write_dialogue_option(
        self, wiki: io.StringIO, indent: str, options: list[act.talk.RogueOptionTalk], confluence: Sequence | None
    ):
        _ = wiki.write(indent)
        _ = wiki.write("{{剧情选项")
        if all(option.trigger_custom_string == options[0].trigger_custom_string for option in options[1:]):
            # 选项的后继全部相同，压成一行即可
            for index, option in enumerate(options):
                assert option.talk_sentence_id is not None
                _ = wiki.write(f"|选项{index + 1}=")
                talk = self._game.talk_sentence_config(option.talk_sentence_id)
                assert talk is not None
                _ = wiki.write(self.__formatter.format(talk.text))
            _ = wiki.write("}}")
            return
        for index, option in enumerate(options):
            assert option.talk_sentence_id is not None
            _ = wiki.write(indent)
            _ = wiki.write(f"|选项{index + 1}=")
            talk = self._game.talk_sentence_config(option.talk_sentence_id)
            assert talk is not None
            _ = wiki.write(self.__formatter.format(talk.text))
            if option.trigger_custom_string is None or option.trigger_custom_string == "":
                continue
            seq = self.__next_custom_string(option.trigger_custom_string)
            if seq is None:
                continue
            if confluence is not None and seq.index != confluence.index:
                _ = wiki.write(indent)
                _ = wiki.write(f"|剧情{index + 1}=")
                self.__wiki_iter_seq(wiki, indent + "  ", seq, confluence)
        _ = wiki.write(indent)
        _ = wiki.write("}}")

    def __write_option(self, wiki: io.StringIO, indent: str, task: Task, confluence: Sequence | None):
        options = list(task.rogue_options())
        if len(options) == 0:
            return
        is_rogue_option = any(option.rogue_option_id is not None for option in options)
        if not is_rogue_option:
            self.__write_dialogue_option(wiki, indent, options, confluence)
            return
        _ = wiki.write(indent)
        _ = wiki.write("{{剧情选项|选项1=选择}}")
        _ = wiki.write(indent)
        _ = wiki.write("{{模拟宇宙事件选项2")
        options.sort(key=lambda option: self.__option_dict[typing.cast(int, option.rogue_option_id)].special is None)
        for index, option in enumerate(options):
            assert option.rogue_option_id is not None
            opt = self.__option_dict[option.rogue_option_id]
            _ = wiki.write(indent)
            title = self.__formatter.format(opt.option.title, opt.desc_value)
            _ = wiki.write(f"|选项{index + 1}=")
            _ = wiki.write(title)
            _ = wiki.write(indent)
            _ = wiki.write(f"|内容{index + 1}=")
            _ = wiki.write(self.__formatter.format(opt.option.desc, opt.desc_value))
            if opt.special is not None:
                _ = wiki.write(indent)
                _ = wiki.write(f"|图标{index + 1}=")
                _ = wiki.write(opt.special.wiki_name)
            _ = wiki.write(indent)
            _ = wiki.write(f"|模式{index + 1}=")
            _ = wiki.write(indent)
            _ = wiki.write(f"|效果{index + 1}=")
            if option.trigger_custom_string is not None and option.trigger_custom_string != "":
                seq = self.__next_custom_string(option.trigger_custom_string)
                if seq is not None and confluence is not None and seq.index != confluence.index:
                    _ = wiki.write(indent)
                    _ = wiki.write(f"|剧情{index + 1}=")
                    _ = wiki.write(indent)
                    _ = wiki.write("  ")
                    _ = wiki.write("{{事件|你|")
                    _ = wiki.write(title)
                    _ = wiki.write("}}")
                    self.__wiki_iter_seq(wiki, indent + "  ", seq, confluence)
        _ = wiki.write(indent)
        _ = wiki.write("}}")

    def __wiki_iter_seq(self, wiki: io.StringIO, indent: str, seq: Sequence, confluence: Sequence | None):
        if confluence is not None and seq.index == confluence.index:
            return
        for task in seq.tasks():
            if task.is_(
                act.task.AdvNpcFaceToPlayer
                | act.task.FinishLevelGraph  # 清空选项，一般在选项结束后有
                | act.task.ShowRogueTalkBg  # 入口
                | act.task.ShowRogueTalkUI  # 入口
                | act.task.SwitchUIMenuBGM  # 循环播放 BGM
                | act.task.TriggerCustomString  # 目前看和改变执行状态有关
                | act.task.TriggerDialogueEvent  # 怀疑和 WaitDialogueEvent 有什么联动，但是所有文件里的 TriggerDialogueEvent 参数都一样
                | act.task.TriggerSound  # 播放声音
                | act.task.TutorialTaskUnlock
                | act.task.WaitCustomString  # 等待 TriggerCustomString
                | act.task.WaitPerformanceEnd  # 出口
                | act.task.WaitRogueSimpleTalkFinish
            ):
                pass
            elif task.is_(act.task.PlayAeonTalk | act.task.PlayRogueSimpleTalk | act.task.PlayAndWaitRogueSimpleTalk):
                self.__write_simple(wiki, indent, task)
            elif task.is_(act.task.PlayRogueOptionTalk):
                next_confluence = self.__find_confluence(seq)
                self.__write_option(wiki, indent, task, next_confluence)
            elif task.is_(act.task.WaitDialogueEvent):
                # TODO: 很重要，但是没搞懂机制
                # 感觉是先随机在几个 SuccessCustomString 里随机选一个，然后开始后续剧情
                pass
            else:
                raise ValueError(f"unknown task type {type(task._task)}")  # pyright: ignore[reportPrivateUsage]
        next_seq = self.__find_confluence(seq)
        if next_seq is not None:
            self.__wiki_iter_seq(wiki, indent, next_seq, confluence)

    def __wiki_debug(self):  # noqa: PLR0912
        for seq in self.__sequences:
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
            print(f"    后继 {[seq.index for seq in self.__find_successors(seq)]}", end="")
            confluence = self.__find_confluence(seq)
            if confluence is not None:
                print(f" 汇聚 {confluence.index}", end="")
            print()
            for task in seq.tasks():
                for talk in task.talks():
                    print("   ", f"{{{{事件|{talk.name}|{talk.text}}}}}")
                for option in task.rogue_options():
                    if option.rogue_option_id is not None:
                        opt = self.__option_dict[option.rogue_option_id]
                        title = self.__formatter.format(opt.option.title, opt.desc_value)
                        desc = self.__formatter.format(opt.option.desc, opt.desc_value)
                        print("   ", f"\033[38;2;242;158;56m{title}\033[39m {desc}", end="")
                        if option.trigger_custom_string is not None:
                            next_seq = self.__next_custom_string(option.trigger_custom_string)
                            if next_seq is not None:
                                print(f" \033[4;38;2;255;255;0mgoto {next_seq.index}\033[39;24m", end="")
                        print()
                    else:
                        assert option.talk_sentence_id is not None
                        talk = self._game.talk_sentence_config(option.talk_sentence_id)
                        assert talk is not None
                        print("   ", f"{talk.name}| {talk.text}")
                if task.is_(act.task.TriggerCustomString):
                    next_seq = self.__next_custom_string(task.trigger_custom_string)
                    if next_seq is not None:
                        print(f"    \033[4;38;2;255;255;0mgoto {next_seq.index}\033[39;24m")
                if isinstance(task._task, act.task.TriggerDialogueEvent):
                    print("    trigger dialogue event", task._task.dialogue_event_id)

    def wiki(self, debug: bool = False) -> str:
        if len(self.__sequences) == 0:
            return ""
        if debug:
            self.__wiki_debug()
        wiki = io.StringIO()
        entrypoint = next(seq for seq in self.__sequences if seq.is_entrypoint)
        self.__wiki_iter_seq(wiki, "\n  ", entrypoint, None)
        return wiki.getvalue()
