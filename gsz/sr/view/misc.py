from __future__ import annotations
import functools
import typing

from .. import excel, view
from .base import View


class ExtraEffectConfig(View[excel.ExtraEffectConfig]):
    """精英组别，属性加成"""

    ExcelOutput: typing.Final = excel.ExtraEffectConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.extra_effect_name)


class RewardData(View[excel.RewardData]):
    ExcelOutput: typing.Final = excel.RewardData

    @functools.cached_property
    def items(self) -> list[view.ItemConfig] | None:
        if self._excel.item_id is None:
            return None
        return list(self._game.item_config_all(filter(None, self._excel.item_id)))


class MazeBuff(View[excel.MazeBuff]):
    ExcelOutput: typing.Final = excel.MazeBuff

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.buff_name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.buff_desc)

    @functools.cached_property
    def param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)


class TextJoinConfig(View[excel.TextJoinConfig]):
    ExcelOutput: typing.Final = excel.TextJoinConfig

    @functools.cached_property
    def default_item(self) -> TextJoinItem:
        item = self._game.text_join_item(self._excel.default_item)
        assert item is not None
        return item

    @functools.cached_property
    def item_list(self) -> list[TextJoinItem]:
        return list(self._game.text_join_item(self._excel.text_join_item_list))


class TextJoinItem(View[excel.TextJoinItem]):
    ExcelOutput: typing.Final = excel.TextJoinItem

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def text(self) -> str:
        if self._excel.text_join_text is None:
            return ""
        return self._game.text(self._excel.text_join_text)
