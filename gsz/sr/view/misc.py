from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc
    import datetime

    from .item import ItemConfig


class ExtraEffectConfig(View[excel.ExtraEffectConfig]):
    """精英组别，属性加成"""

    ExcelOutput: typing.Final = excel.ExtraEffectConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.extra_effect_name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.extra_effect_desc)

    @property
    def desc_param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.desc_param_list)


class LoopCGConfig(View[excel.LoopCGConfig]):
    ExcelOutput: typing.Final = excel.LoopCGConfig

    @property
    def path(self) -> str:
        return self._excel.video_path


class MazeBuff(View[excel.MazeBuff]):
    ExcelOutput: typing.Final = excel.MazeBuff

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.buff_name)

    @property
    def level(self) -> int:
        return self._excel.lv

    @property
    def level_max(self) -> int:
        return self._excel.lv_max

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.buff_desc)

    @functools.cached_property
    def simple_desc(self) -> str:
        return "" if self._excel.buff_simple_desc is None else self._game.text(self._excel.buff_simple_desc)

    @functools.cached_property
    def param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)


class RewardData(View[excel.RewardData]):
    ExcelOutput: typing.Final = excel.RewardData

    @functools.cached_property
    def __items(self) -> list[ItemConfig | None]:
        if self._excel.item_id is None:
            return []
        items: list[ItemConfig | None] = []
        for item_id in self._excel.item_id:
            if item_id is None:
                items.append(None)
                continue
            item = self._game.item_config_all(item_id)
            assert item is not None
            items.append(item)
        return items

    def items(self) -> collections.abc.Iterable[ItemConfig | None]:
        from .item import ItemConfig

        return (None if item is None else ItemConfig(self._game, item._excel) for item in self.__items)


class ScheduleData(View[excel.ScheduleData]):
    ExcelOutput: typing.Final = excel.ScheduleData

    @property
    def begin_time(self) -> datetime.datetime:
        return self._excel.begin_time

    @property
    def end_time(self) -> datetime.datetime:
        return self._excel.end_time

    def contains(self, datetime: datetime.datetime) -> bool:
        return self.begin_time <= datetime < self.end_time


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
