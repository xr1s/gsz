from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import pathlib

    from ..act import Act


class Performance(View[excel.Performance]):
    ExcelOutput: typing.Final = excel.Performance

    @property
    def performance_path(self) -> pathlib.Path | None:
        if self._excel.performance_path == "":
            return None
        return self._game.base.joinpath(self._excel.performance_path.strip())

    @functools.cached_property
    def __performance(self) -> Act | None:
        from ..act import Act

        return None if self.performance_path is None else Act(self._game, self.performance_path)

    def performance(self) -> Act | None:
        from ..act import Act

        return None if self.__performance is None else Act(self._game, self.__performance._act)  # pyright: ignore[reportPrivateUsage]
