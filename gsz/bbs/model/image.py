import enum

import pydantic

from .base import Model


class Format(enum.Enum):
    _ = ""
    GIF = "gif"
    JPG = "jpg"
    PNG = "png"
    Webp = "webp"


class Crop(Model):
    x: int
    y: int
    w: int
    h: int
    url: pydantic.HttpUrl


class EntityType(enum.Enum):
    Post = "IMG_ENTITY_POST"
    Unknown = "IMG_ENTITY_UNKNOWN"


class Image(Model):
    url: pydantic.HttpUrl
    height: int
    width: int
    format: Format
    size: int
    crop: Crop | None = None
    is_user_set_cover: bool
    image_id: int
    entity_type: EntityType
    entity_id: int
    is_deleted: bool
