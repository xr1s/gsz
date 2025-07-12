from __future__ import annotations

import functools
import io
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from ..excel import item
    from .misc import RewardData


class ItemConfig(View[excel.ItemConfig]):
    """道具"""

    ExcelOutput: typing.Final = excel.ItemConfig

    @functools.cached_property
    def name(self) -> str:
        if self._excel.item_name is None:
            return ""
        return self._game.text(self._excel.item_name)

    @functools.cached_property
    def wiki_name(self) -> str:
        return self._game._plain_formatter.format(self.name)  # pyright: ignore[reportPrivateUsage]

    @functools.cached_property
    def icon_path(self) -> str:
        return self._excel.item_figure_icon_path

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

    @property
    def use_method(self) -> item.UseMethod | None:
        return self._excel.use_method

    @functools.cached_property
    def __purpose(self) -> ItemPurpose | None:
        if self._excel.purpose_type is None:
            return None
        purpose = self._game.item_purpose(self._excel.purpose_type)
        assert purpose is not None
        return purpose

    def purpose(self) -> ItemPurpose | None:
        return None if self.__purpose is None else ItemPurpose(self._game, self.__purpose._excel)

    @functools.cached_property
    def __use_data(self) -> ItemUseData | None:
        return self._game.item_use_data(self._excel.id)

    def use_data(self) -> ItemUseData | None:
        return None if self.__use_data is None else ItemUseData(self._game, self.__use_data._excel)

    @functools.cached_property
    def __cure_info_data(self) -> ItemCureInfoData | None:
        return self._game.item_cure_info_data(self._excel.id)

    def cure_info_data(self) -> ItemCureInfoData | None:
        return None if self.__cure_info_data is None else ItemCureInfoData(self._game, self.__cure_info_data._excel)


class ItemCureInfoData(View[excel.ItemCureInfoData]):
    ExcelOutput: typing.Final = excel.ItemCureInfoData

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.cure_info_title)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.cure_info_desc)

    @property
    def img_path(self) -> str:
        return self._excel.img_path

    def wiki(self) -> str:
        wiki = io.StringIO()
        _ = wiki.write("<!-- 剧情 -->\n{{书籍/分卷|\n名称=")
        _ = wiki.write(self.title)
        _ = wiki.write("\n|卷数=1\n|实装版本=\n|获取方式=\n|内容=\n")
        if self.img_path != "":
            _ = wiki.write(f"<!-- {self.img_path} -->\n")
        _ = wiki.write(self._game._mw_pretty_formatter.format(self.desc))  # pyright: ignore[reportPrivateUsage]
        _ = wiki.write("\n}}")
        return wiki.getvalue()


class ItemPurpose(View[excel.ItemPurpose]):
    ExcelOutput: typing.Final = excel.ItemPurpose

    @property
    def id(self) -> int:
        return self._excel.id_

    @functools.cached_property
    def text(self) -> str:
        return self._game.text(self._excel.purpose_text)


class ItemUseData(View[excel.ItemUseData]):
    ExcelOutput: typing.Final = excel.ItemUseData

    @functools.cached_property
    def __rewards(self) -> list[RewardData]:
        return list(self._game.reward_data(self._excel.use_param))

    def rewards(self) -> collections.abc.Iterable[RewardData]:
        from .misc import RewardData

        return (RewardData(self._game, reward._excel) for reward in self.__rewards)
