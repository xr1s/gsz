from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ..data import GameData
    from ..view.rogue import RogueDialogueDynamicDisplay, RogueDialogueOptionDisplay, RogueEventSpecialOption


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

    def option(self) -> RogueDialogueOptionDisplay:
        from ..view import RogueDialogueOptionDisplay

        return RogueDialogueOptionDisplay(self._game, self.__option._excel)  # pyright: ignore[reportPrivateUsage]

    @property
    def special(self) -> RogueEventSpecialOption | None:
        if self.__special is None:
            return None
        from ..view import RogueEventSpecialOption

        return RogueEventSpecialOption(self._game, self.__special._excel)  # pyright: ignore[reportPrivateUsage]

    @property
    def dynamic(self) -> list[RogueDialogueDynamicDisplay]:
        from ..view import RogueDialogueDynamicDisplay

        return [RogueDialogueDynamicDisplay(self._game, dynamic._excel) for dynamic in self.__dynamic]  # pyright: ignore[reportPrivateUsage]

    @property
    def desc_value(self) -> list[int | str]:
        return self.__desc_value
