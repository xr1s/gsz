import enum
import typing

import pydantic
import pydantic_extra_types.color

from . import image, vod
from .base import GameId, Model


class Align(enum.Enum):
    Center = "center"
    Justify = "justify"
    Right = "right"


class TextAttributesList(enum.Enum):
    Bullet = "bullet"


class Attributes(Model):
    align: Align | None = None
    bold: bool = False
    color: (
        pydantic_extra_types.color.Color
        | typing.Literal["inherit", "windowtext", "var(--default-dark-color-85)"]
        | None
    ) = None
    header: int | None = None
    italic: bool = False
    list: TextAttributesList | None = None
    # 可能是 http 链接，也可能是邮件链接 mailto:
    # 还可能是 relative 地址
    link: str | None = None
    # 图片类型 StructuredContent 属性
    height: int | None = None
    width: int | None = None
    size: int | None = None
    ext: image.Format | None = None


class Divider(Model):
    class Divider(enum.Enum):
        """类似 <HR> 但是实际上是图片的分割线"""

        Line1 = "line_1"
        """
        中间为米游兔（应用 Logo 上的吉祥物），两侧虚线
        https://upload-bbs.miyoushe.com/upload/2021/01/05/40eb5281cb24042bf34a9f1bcc61eaf5.png
        """
        Line2 = "line_2"
        """
        中间为米游兔（应用 Logo 上的吉祥物），两侧渐隐实线
        https://upload-bbs.miyoushe.com/upload/2021/01/05/477d4c535e965bec1791203aecdfa8e6.png
        """
        Line3 = "line_3"
        """
        花里胡哨的，左边米游姬，右边米游兔，中间用类似链条的十字和星球串起来
        https://upload-bbs.miyoushe.com/upload/2021/01/05/e7047588e912d60ff87a975e037c7606.png
        """
        Line4 = "line_4"
        """
        非常朴素的一条实线
        https://upload-bbs.miyoushe.com/upload/2022/07/13/line_4.png
        """

    divider: Divider


class Image(Model):
    image: pydantic.HttpUrl | typing.Literal["true"]


class LinkCard(Model):
    class Card(Model):
        link_type: int
        origin_url: pydantic.HttpUrl
        landing_url: pydantic.HttpUrl
        cover: pydantic.HttpUrl
        title: str
        card_id: int
        card_status: int
        market_price: str | None = None
        """目前看未定事件簿专属，带价格的米游铺链接"""
        price: str | None = None
        """目前看未定事件簿专属，带价格的米游铺链接"""
        button_text: str | None = None
        """目前看未定事件簿专属，带价格的米游铺链接"""
        landing_url_type: int | None = None

    link_card: Card


class Lottery(Model):
    class Lottery(Model):
        id: str
        toast: str

    backup_text: str
    lottery: Lottery


def validate_twice(value: bytes) -> list["StructuredContent"] | None:
    if len(value) == 0:
        return None
    return pydantic.TypeAdapter(list[StructuredContent]).validate_json(value)


class Fold(Model):
    """折叠内容"""

    class Fold(Model):
        title: typing.Annotated[list["StructuredContent"], pydantic.BeforeValidator(validate_twice)]
        content: typing.Annotated[list["StructuredContent"], pydantic.BeforeValidator(validate_twice)]
        id: pydantic.UUID4
        size: int

    backup_text: str
    fold: Fold


class Mention(Model):
    """@somebody"""

    class Mention(Model):
        uid: int
        nickname: str

    mention: Mention


class ReceptionCard(Model):
    class PreRegisterCount(Model):
        count: int

    class Pkg(Model):
        android_url: pydantic.HttpUrl
        pkg_name: str
        pkg_version: str
        ios_url: pydantic.AnyUrl
        pkg_length: int
        pkg_md5: typing.Annotated[bytes, pydantic.BeforeValidator(bytes.fromhex)]
        pkg_version_code: int
        ios_version: str
        filename: str
        ios_scheme_url: pydantic.AnyUrl

    class UserStatus(Model):
        is_device_support: bool
        pre_register_status: typing.Literal[2]
        has_qualification: bool
        qualify_type: typing.Literal[1]

    class Card(Model):
        id: int
        game_id: GameId
        name: str
        icon: pydantic.HttpUrl
        game_reception_status: typing.Literal[4]
        pre_register_count: "ReceptionCard.PreRegisterCount"
        prompt: str
        custom_toast: str
        pkg: "ReceptionCard.Pkg"
        user_status: "ReceptionCard.UserStatus"

    backup_text: str
    reception_card: Card


class Video(Model):
    video: pydantic.HttpUrl


class VillaCard(Model):
    class Room(Model):
        room_id: int
        room_name: str
        sender_avatar_list: list[pydantic.HttpUrl]
        sender_num: int

    class Card(Model):
        villa_id: int
        villa_name: str
        villa_avatar_url: pydantic.HttpUrl
        villa_cover: pydantic.HttpUrl
        owner_uid: int
        owner_nickname: str
        owner_avatar_url: pydantic.HttpUrl
        villa_introduce: str
        tag_list: list[str]
        villa_member_num: int
        is_official: bool
        is_available: bool
        hot_member_avatar: list[pydantic.HttpUrl]
        hot_room: "VillaCard.Room"

    villa_card: Card


class VillaRoomCard(Model):
    class Card(Model):
        room_id: int
        room_name: str
        room_type: typing.Literal["RoomTypeChatRoom"]
        villa_id: int
        villa_name: str
        villa_avatar_url: pydantic.HttpUrl
        active_member_num: int
        active_user_avatar: list[pydantic.HttpUrl]
        is_available: bool

    villa_room_card: Card


class Vod(Model):
    vod: vod.Vod


class Vote(Model):
    class Vote(Model):
        id: int
        uid: int

    vote: Vote


class StructuredContent(Model):
    insert: (
        str
        | Divider
        | Image
        | LinkCard
        | Lottery
        | Fold
        | Mention
        | ReceptionCard
        | Video
        | VillaCard
        | VillaRoomCard
        | Vod
        | Vote
    )
    attributes: Attributes | None = None
