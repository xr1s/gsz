from .base import Model, Text


class BookDisplayType(Model):
    book_display_type_id: int
    alignment: int

    @property
    def id(self) -> int:
        return self.book_display_type_id


class BookSeriesConfig(Model):
    book_series_id: int
    book_series: Text
    book_series_comments: Text | None = None
    book_series_num: int
    book_series_world: int
    is_show_in_bookshelf: bool = False

    @property
    def id(self) -> int:
        return self.book_series_id


class BookSeriesWorld(Model):
    book_series_world: int
    book_series_world_textmap_id: Text
    book_series_world_icon_path: str
    book_series_world_background_path: str

    @property
    def id(self) -> int:
        return self.book_series_world


class LocalbookConfig(Model):
    book_id: int
    book_series_id: int
    book_series_inside_id: int
    book_inside_name: Text
    book_content: Text
    book_display_type: int
    local_book_image_path: list[str]

    @property
    def id(self) -> int:
        return self.book_id
