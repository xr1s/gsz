from __future__ import annotations
import functools
import re

from .. import excel
from .base import View


class BookDisplayType(View[excel.BookDisplayType]):
    type ExcelOutput = excel.BookSeriesConfig


class BookSeriesConfig(View[excel.BookSeriesConfig]):
    type ExcelOutput = excel.BookSeriesConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.book_series).replace("<unbreak>", "").replace("</unbreak>", "")

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def comments(self) -> str | None:
        if self._excel.book_series_comments is None:
            return None
        return self._game.text(self._excel.book_series_comments)

    @functools.cached_property
    def world(self) -> BookSeriesWorld:
        world = self._game.book_series_world(self._excel.book_series_world)
        assert world is not None
        return world

    @functools.cached_property
    def books(self) -> list[LocalbookConfig]:
        books = self._game._book_series_localbook.get(self.id, ())  # pyright: ignore[reportPrivateUsage]
        return [LocalbookConfig(self._game, excel) for excel in books]

    @property
    def is_show_in_bookshelf(self) -> bool:
        return self._excel.is_show_in_bookshelf

    @property
    def num(self) -> int:
        return self._excel.book_series_num

    @functools.cached_property
    def __book_type(self) -> str:  # noqa: PLR0911, PLR0912
        item = self._game.item_config_book(self.books[0].id)
        if item is None:
            item = self._game.item_config(self.books[0].id)
        if item is None:
            return "资料"  #  大地图或者剧情中散落的阅读物
        [_file_path, file_name] = item.icon_path.rsplit("/", 1)
        [file_stem, _file_ext] = file_name.rsplit(".", 1)
        match int(file_stem):
            # 按顺序分别是 雅利洛 | 空间站黑塔 | 仙舟罗浮 | 匹诺康尼
            # 特殊图标单独备注
            case 190001 | 190004 | 190007 | 190016 | 190017:
                return "书籍"
            case 190002 | 190005 | 190008 | 190015 | 190018:
                return "资料"
            case 190003 | 190006 | 190009:
                return "信件"
            case 140236:  # 目前只有罗浮的《钟珊的来信》和匹诺康尼的《关于财富学院代表的联名投诉信》
                return "信件2"
            case 190010 | 190020:  # 只出现在罗浮、翁法罗斯
                return "石碑"
            case 190011:  # 只出现在罗浮
                return "拓印"
            case 190012:  # 只出现在罗浮
                return "如意"
            case 190013:  # 只出现在匹诺康尼
                return "便条"
            case 190014:  # 只出现在匹诺康尼
                return "录像带"
            case 190019:  # 只出现在翁法罗斯
                return "回响"
            case _:
                raise ValueError("可能是新版本新增不同类型的图书 {} {}", self.name, file_stem)

    def wiki(self) -> str:
        return self._game._template_environment.get_template("book-series.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            series=self, book_type=self.__book_type
        )


class BookSeriesWorld(View[excel.BookSeriesWorld]):
    type ExcelOutput = excel.BookSeriesWorld

    @property
    def id(self) -> int:
        return self._excel.book_series_world


class LocalbookConfig(View[excel.LocalbookConfig]):
    type ExcelOutput = excel.LocalbookConfig

    __UNBREAK_TAG: re.Pattern[str] = re.compile("</?unbreak>")

    @functools.cached_property
    def name(self) -> str:
        return self._game._plain_formatter.format(self._game.text(self._excel.book_inside_name))  # pyright: ignore[reportPrivateUsage]

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def series(self) -> BookSeriesConfig:
        series = self._game.book_series_config(self._excel.book_series_id)
        assert series is not None
        return series

    @functools.cached_property
    def content(self) -> str:
        return self._game.text(self._excel.book_content)

    @property
    def image_path(self) -> list[str]:
        return self._excel.local_book_image_path
