from __future__ import annotations

import functools
import typing

from gsz.gi.view import avatar

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    from . import avatar


class Npc(View[excel.Npc]):
    ExcelBinOutput: typing.Final = excel.Npc

    @property
    def id(self) -> int:
        return self._excel.id_

    @functools.cached_property
    def __avatar(self) -> avatar.Avatar | None:
        if self._excel.avatar_id == 0:
            return None
        avatar = self._game.avatar(self._excel.avatar_id)
        assert avatar is not None
        return avatar

    def avatar(self) -> avatar.Avatar | None:
        from .avatar import Avatar

        return Avatar(self._game, self.__avatar._excel) if self.__avatar is not None else None

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name_text_map_hash)
