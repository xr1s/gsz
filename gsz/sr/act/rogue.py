from __future__ import annotations

import functools
import typing

import typing_extensions

from . import model, wiki

if typing.TYPE_CHECKING:
    import collections.abc
    import io
    import pathlib

    from ..data import GameData
    from ..view.rogue import RogueDialogueDynamicDisplay
    from .act import Act
    from .option import Option
    from .sequence import Sequence
    from .task import Task


class Dialogue(wiki.Dialogue):
    def __init__(self, game: GameData, excel: model.Dialogue):
        self._game: GameData = game
        self._dialogue: model.Dialogue = excel

    @property
    def progress(self) -> int | None:
        return self._dialogue.dialogue_progress

    @functools.cached_property
    def dialogue_path(self) -> pathlib.Path:
        return self._game.base / self._dialogue.dialogue_path.strip()

    @functools.cached_property
    def __dialogue(self) -> model.Act:
        return model.Act.model_validate_json(self.dialogue_path.read_bytes())

    def dialogue(self) -> Act:
        from .act import Act

        return Act(self._game, self.__dialogue)

    @functools.cached_property
    def option_path(self) -> pathlib.Path | None:
        return None if self._dialogue.option_path is None else self._game.base / self._dialogue.option_path.strip()

    @functools.cached_property
    def __opt(self) -> model.Opt | None:
        if self.option_path is None:
            return None
        return model.Opt.model_validate_json(self.option_path.read_bytes())

    @functools.cached_property
    def __options(self) -> list[Option]:
        from .option import Option

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

    def options(self) -> collections.abc.Iterable[Option]:
        from .option import Option

        return (
            Option(self._game, option.id, option.option(), option.special, list(option.dynamic), option.desc_value)
            for option in self.__options
        )

    @functools.cached_property
    @typing_extensions.override
    def _sequences(self) -> list[Sequence]:
        from .sequence import Sequence

        if self.__dialogue.on_start_sequece is None:
            return []
        return [Sequence(self._game, seq, index) for index, seq in enumerate(self.__dialogue.on_start_sequece)]

    def _write_rogue_options(
        self,
        style: wiki.WikiStyle,
        wiki: io.StringIO,
        indent: str,
        options: list[model.talk.RogueOptionTalk],
        confluence: Sequence | None,
    ):
        _ = wiki.write(indent)
        _ = wiki.write("{{剧情选项|选项1=选择}}")
        _ = wiki.write(indent)
        _ = wiki.write("{{模拟宇宙事件选项2")
        options.sort(key=lambda option: self.__option_dict[typing.cast(int, option.rogue_option_id)].special is None)
        for index, option in enumerate(options):
            assert isinstance(option, model.talk.RogueOptionTalk)
            number = index + 1
            assert option.rogue_option_id is not None
            opt = self.__option_dict[option.rogue_option_id]
            _ = wiki.write(indent)
            rogue_option = opt.option()
            title = self._formatter.format(rogue_option.title, opt.desc_value)
            _ = wiki.write(f"|选项{number}=")
            _ = wiki.write(title)
            _ = wiki.write(indent)
            _ = wiki.write(f"|内容{number}=")
            _ = wiki.write(self._formatter.format(rogue_option.desc, opt.desc_value))
            if opt.special is not None:
                _ = wiki.write(indent)
                _ = wiki.write(f"|图标{number}=")
                _ = wiki.write(opt.special.wiki_name)
            _ = wiki.write(indent)
            _ = wiki.write(f"|模式{number}=")
            _ = wiki.write(indent)
            _ = wiki.write(f"|效果{number}=")
            if option.trigger_custom_string is not None and option.trigger_custom_string != "":
                seq = self._next_custom_string(option.trigger_custom_string)
                if seq is None:
                    continue  # 找不到后继
                if confluence is not None and seq.index == confluence.index:
                    continue  # 后继是汇聚点
                if self._seq_in_search_stack[seq.index]:
                    continue  # 后继已经深搜过了
                _ = wiki.write(indent)
                _ = wiki.write(f"|剧情{number}=")
                _ = wiki.write(indent)
                _ = wiki.write("  ")
                _ = wiki.write("{{事件|你|")
                _ = wiki.write(title)
                _ = wiki.write("}}")
                self._seq_in_search_stack[seq.index] = True
                self._wiki_iter_seq(style, wiki, indent + "  ", seq, confluence)
                self._seq_in_search_stack[seq.index] = False
        _ = wiki.write(indent)
        _ = wiki.write("}}")

    @typing_extensions.override
    def _write_option(
        self, style: wiki.WikiStyle, wiki: io.StringIO, indent: str, task: Task, confluence: Sequence | None
    ):
        options = list(task.options())
        if len(options) == 0:
            return
        is_rogue_option = all(
            isinstance(option, model.talk.RogueOptionTalk) and option.rogue_option_id is not None for option in options
        )
        if not is_rogue_option:
            self._write_dialogue_option(style, wiki, indent, options, confluence)
            return
        self._write_rogue_options(
            style, wiki, indent, typing.cast(list[model.talk.RogueOptionTalk], options), confluence
        )

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
                    assert isinstance(option, model.talk.RogueOptionTalk)
                    if option.rogue_option_id is not None:
                        opt = self.__option_dict[option.rogue_option_id]
                        rogue_option = opt.option()
                        title = self._formatter.format(rogue_option.title, opt.desc_value)
                        desc = self._formatter.format(rogue_option.desc, opt.desc_value)
                        print("   ", f"\033[38;2;242;158;56m{title}\033[39m {desc}", end="")
                        if option.trigger_custom_string is not None:
                            next_seq = self._next_custom_string(option.trigger_custom_string)
                            if next_seq is not None:
                                print(f" \033[4;38;2;255;255;0mgoto {next_seq.index}\033[39;24m", end="")
                        print()
                    else:
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

    @functools.cached_property
    def __need_debug(self) -> bool:
        return any(task.is_(model.task.WaitDialogueEvent) for seq in self._sequences for task in seq.tasks())

    @typing_extensions.override
    def wiki(self, *, debug: bool = False, style: wiki.WikiStyle = wiki.WikiStyle.Rogue) -> str:
        if len(self._sequences) == 0:
            return ""
        if debug or self.__need_debug:
            self.__wiki_debug()
        return super().wiki(style=style)
