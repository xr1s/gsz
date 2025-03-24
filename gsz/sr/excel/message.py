import enum
import pathlib
import typing

import typing_extensions

from .base import ModelID, Text


class EmojiGender(enum.Enum):
    All = "All"
    Female = "Female"
    Male = "Male"


class EmojiConfig(ModelID):
    emoji_id: int
    gender: EmojiGender
    emoji_group_id: int | None = None
    key_words: Text
    emoji_path: str
    same_group_order: int | None = None
    gender_link: int | None = None
    is_train_members: bool = False

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.emoji_id


class EmojiGroup(ModelID):
    emoji_group_id: int
    emoji_group_type: typing.Literal["All"]
    group_name: Text
    img_path: pathlib.Path

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.emoji_group_id


class MessageContactsCamp(ModelID):
    contacts_camp: int
    name: Text
    sort_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.contacts_camp


class MessageContactsConfig(ModelID):
    id_: int
    name: Text
    icon_path: str
    signature_text: Text | None = None
    contacts_type: int | None = None
    contacts_camp: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class MessageContactsType(ModelID):
    contacts_type: int
    name: Text
    sort_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.contacts_type


class MessageGroupConfig(ModelID):
    id_: int
    message_contacts_id: int
    message_section_id_list: list[int]
    activity_module_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class Sender(enum.Enum):
    NPC = "NPC"
    Player = "Player"
    PlayerAuto = "PlayerAuto"
    System = "System"


class ItemType(enum.Enum):
    Image = "Image"
    """
    目前只有四个，罗浮杂俎新阶段任务小桂子发的短信
    MessageItemLink.json 中找对应条目
    """
    Link = "Link"
    """
    目前只有两个，穿插在首次抵达罗浮主线时候丹恒视角的故事
    MessageItemRaidEntrance.json 中找对应条目
    """
    Raid = "Raid"
    Sticker = "Sticker"
    Text = "Text"
    Video = "Video"


class MessageItemConfig(ModelID):
    id_: int
    contacts_id: int | None = None
    sender: Sender
    item_type: ItemType
    main_text: Text | None = None
    item_content_id: int | None = None
    item_image_id: int | None = None
    option_text: Text | None = None
    next_item_id_list: list[int]
    section_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class MessageItemImage(ModelID):
    id_: int
    image_path: str
    female_image_path: str | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class MessageItemLink(ModelID):
    id_: int
    title: Text
    image_path: str
    type: typing.Literal["Exit"]
    once_only: typing.Literal[True]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class MessageItemRaidEntrance(ModelID):
    id_: int
    raid_id: int
    image_path: str
    invalid_mission_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class MessageItemVideo(ModelID):
    id_: int
    image_path: str
    video_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class MessageSectionConfig(ModelID):
    id_: int
    start_message_item_id_list: list[int]
    is_perform_message: bool = False
    main_mission_link: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
