from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    from ..excel import item


class ItemConfig(View[excel.ItemConfig]):
    """道具"""

    type ExcelOutput = excel.ItemConfig

    @functools.cached_property
    def name(self) -> str:
        if self._excel.item_name is None:
            return ""
        return self._game._plain_formatter.format(self._game.text(self._excel.item_name))  # pyright: ignore[reportPrivateUsage]

    @functools.cached_property
    def icon_path(self) -> str:
        return self._excel.item_icon_path

    @functools.cached_property
    def desc(self) -> str:
        if self._excel.item_desc is None:
            return ""
        return self._game.text(self._excel.item_desc)

    @functools.cached_property
    def bg_desc(self) -> str:
        if self._excel.item_bg_desc is None:
            return ""
        return self._game.text(self._excel.item_bg_desc)

    @property
    def rarity(self) -> item.Rarity:
        return self._excel.rarity

    @property
    def main_type(self) -> item.MainType:
        return self._excel.item_main_type

    @property
    def sub_type(self) -> item.SubType:
        return self._excel.item_sub_type


class ItemPurpose(View[excel.ItemPurpose]):
    type ExcelOutput = excel.ItemPurpose
