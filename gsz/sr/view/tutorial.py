from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View


class TutorialGuideData(View[excel.TutorialGuideData]):
    ExcelOutput: typing.Final = excel.TutorialGuideData

    @functools.cached_property
    def desc(self) -> str:
        return "" if self._excel.desc_text is None else self._game.text(self._excel.desc_text)


class TutorialGuideGroup(View[excel.TutorialGuideGroup]):
    ExcelOutput: typing.Final = excel.TutorialGuideGroup

    @functools.cached_property
    def message(self) -> str:
        return "" if self._excel.message_text is None else self._game.text(self._excel.message_text)

    @functools.cached_property
    def __datas(self) -> list[TutorialGuideData]:
        datas = (self._game.tutorial_guide_data(guide_id) for guide_id in self._excel.tutorial_guide_id_list)
        return list(filter(None, datas))

    @functools.cached_property
    def datas(self) -> list[TutorialGuideData]:
        return [TutorialGuideData(self._game, data._excel) for data in self.__datas]
