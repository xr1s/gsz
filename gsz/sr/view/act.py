from __future__ import annotations
import functools
import io
import itertools
import typing

from .. import act
from ..act import task


if typing.TYPE_CHECKING:
    import collections.abc
    import pathlib
    from .rogue import RogueDialogueDynamicDisplay, RogueDialogueOptionDisplay, RogueEventSpecialOption
    from .talk import TalkSentenceConfig
    from ..data import GameData


class Act:
    def __init__(self, game: GameData, excel: pathlib.Path | act.Act):
        self._game: GameData = game
        self._act: act.Act = (
            excel if isinstance(excel, act.Act) else act.Act.model_validate_json(game.base.joinpath(excel).read_bytes())
        )

    @functools.cached_property
    def __tasks(self) -> list[act.Task]:
        return [task for seq in self._act.on_start_sequece for task in seq.task_list]

    def tasks(self) -> collections.abc.Iterable[Task]:
        return (Task(self._game, task) for task in self.__tasks)


class Task:
    def __init__(self, game: GameData, excel: act.Task):
        self._game: GameData = game
        self._task: act.Task = excel

    @property
    def custom_string(self) -> str:
        if isinstance(self._task, task.WaitCustomString):
            return self._task.custom_string.value
        return ""

    @functools.cached_property
    def __talks(self) -> list[TalkSentenceConfig]:
        if isinstance(self._task, task.PlayRogueSimpleTalk | task.PlayAndWaitRogueSimpleTalk | task.PlayAeonTalk):
            return list(self._game.talk_sentence_config(talk.talk_sentence_id for talk in self._task.simple_talk_list))
        return []

    def talks(self) -> collections.abc.Iterable[TalkSentenceConfig]:
        from .talk import TalkSentenceConfig

        return [TalkSentenceConfig(self._game, talk._excel) for talk in self.__talks]  # pyright: ignore[reportPrivateUsage]


class Option:
    def __init__(
        self,
        game: GameData,
        option: RogueDialogueOptionDisplay,
        special: RogueEventSpecialOption | None,
        dynamic: list[RogueDialogueDynamicDisplay],
        desc_value: list[int | str],
    ):
        self._game: GameData = game
        self.__option = option
        self.__special = special
        self.__dynamic = dynamic
        self.__desc_value = desc_value

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
        return self._game.base / self._dialogue.dialogue_path

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
                if len(desc_value) != 1:  # desc_value 传入作为 #5
                    desc_value.append("")
                desc_value.append(opt.desc_value)
            if opt.desc_value2 is not None:
                while len(desc_value) < 4:  # desc_value2 传入作为 #5
                    desc_value.append("")
                desc_value.append(opt.desc_value2)
            if opt.desc_value3 is not None:  # desc_value3 传入作为 #6
                while len(desc_value) < 5:
                    desc_value.append("")
                desc_value.append(opt.desc_value3)
            if opt.desc_value4 is not None:  # desc_value4 传入作为 #7
                while len(desc_value) < 6:
                    desc_value.append("")
                desc_value.append(opt.desc_value4)
            options.append(Option(self._game, option, special, dynamic, desc_value))
        return options

    def option(self) -> collections.abc.Iterable[Option]:
        return (
            Option(self._game, option.option, option.special, list(option.dynamic), option.desc_value)
            for option in self.__options
        )

    @property
    def __formatter(self):
        from ...format import Formatter, Syntax

        return Formatter(syntax=Syntax.MediaWiki, game=self._game, percent_as_plain=True)

    def wiki(self) -> str:
        text = io.StringIO()
        talks = itertools.chain.from_iterable(task.talks() for task in self.dialogue().tasks())
        for talk in talks:
            _ = text.write("{{事件|")
            _ = text.write(self.__formatter.format(talk.name))
            _ = text.write("|")
            _ = text.write(self.__formatter.format(talk.text))
            _ = text.write("}}\n")
        _ = text.write("{{模拟宇宙事件选项2")
        for index, opt in enumerate(self.__options):
            _ = text.write(f"\n|选项{index + 1}=")
            _ = text.write(self.__formatter.format(opt.option.title, opt.desc_value))
            _ = text.write(f"\n|内容{index + 1}=")
            _ = text.write(self.__formatter.format(opt.option.desc, opt.desc_value))
            if opt.special is not None:
                _ = text.write(f"\n|图标{index + 1}=")
                _ = text.write(opt.special.wiki_name)
        _ = text.write("\n}}")
        return text.getvalue()
