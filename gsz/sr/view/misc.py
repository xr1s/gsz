from __future__ import annotations
import functools

from .. import excel
from .base import View


class ExtraEffectConfig(View[excel.ExtraEffectConfig]):
    """精英组别，属性加成"""

    type ExcelOutput = excel.ExtraEffectConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.extra_effect_name)


class TextJoinConfig(View[excel.TextJoinConfig]):
    type ExcelOutput = excel.TextJoinConfig

    @functools.cached_property
    def default_item(self) -> TextJoinItem:
        item = self._game.text_join_item(self._excel.default_item)
        assert item is not None
        return item

    @functools.cached_property
    def item_list(self) -> list[TextJoinItem]:
        return list(self._game.text_join_item(self._excel.text_join_item_list))


class TextJoinItem(View[excel.TextJoinItem]):
    type ExcelOutput = excel.TextJoinItem

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def text(self) -> str:
        if self._excel.text_join_text is None:
            return ""
        return self._game.text(self._excel.text_join_text)
