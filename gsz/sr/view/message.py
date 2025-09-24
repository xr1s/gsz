from __future__ import annotations

import abc
import collections
import collections.abc
import functools
import io
import typing

import typing_extensions

from .. import excel
from ..excel import message
from .base import View

if typing.TYPE_CHECKING:
    from ...format import Formatter
    from ..data import GameData
    from .mission import MainMission


class EmojiConfig(View[excel.EmojiConfig]):
    ExcelOutput: typing.Final = excel.EmojiConfig

    @property
    def id(self) -> int:
        return self._excel.id

    __WIKI_MAPPING: dict[int, str] = {
        # 隐藏，仅用于游戏内短信，不可用于玩家之间私聊短信
        30101: "00-01",  # 布洛妮娅（短信对象）-干杯
        30102: "00-02",  # 布洛妮娅（短信对象）-鲜花
        30001: "00-03",  # 艾丝妲（短信对象）-坏笑
        30002: "00-04",  # 阿兰（短信对象）-威胁
        30014: "00-05",  # 花火（短信对象）-照片
        30015: "00-06",  # 花火（短信对象）-照片
        30016: "00-07",  # 花火（短信对象）-照片
        # 帕姆展览馆第1弹 三月七
        101002: "01-01",  # 能量发射
        101003: "01-14",  # 点赞
        101005: "01-16",  # 悄悄话
        30006: "01-15",  # 生气
        101006: "01-11",  # 盯
        30004: "01-09",  # 骄傲
        101007: "01-10",  # 加油
        30005: "01-07",  # 哭
        30003: "01-03",  # 暗中观察
        # 帕姆展览馆第2弹 漫游测试篇
        102001: "02-01",  # 丹恒-思考
        102002: "02-02",  # 姬子-笑
        30007: "02-11",  # 银狼-吹泡泡
        # 帕姆展览馆第3弹 跃迁测试篇
        30201: "03-05",  # 刃-来了
        103002: "03-11",  # 彦卿-哼
        103004: "03-15",  # 星-吃瓜
        103007: "03-09",  # 驭空-叹气
        103013: "03-07",  # 素裳-冲鸭
        # 帕姆展览馆第5弹 呜呜伯
        106001: "05-01",  # 委屈
        106002: "05-02",  # 惊吓
        106003: "05-03",  # 开心
        106004: "05-10",  # 睡觉
        106005: "05-12",  # 比心
        106006: "05-15",  # 无奈
        106007: "05-09",  # 无语
        106008: "05-11",  # 点赞
        106009: "05-16",  # 晕
        106010: "05-05",  # 气气
        106011: "05-06",  # 疑惑
        106012: "05-14",  # 恶作剧
        106013: "05-08",  # 坏笑
        106014: "05-07",  # 期待
        106015: "05-04",  # 认真
        106016: "05-13",  # 敲黑板
        # 帕姆展览馆第7弹 帕姆篇
        20001: "07-01",  # 嗨
        20002: "07-07",  # 比心
        20003: "07-08",  # 不可以
        20004: "07-03",  # 收到
        20005: "07-04",  # 哭哭
        20006: "07-02",  # 点赞
        20007: "07-05",  # 疑惑
        20008: "07-06",  # 震惊
        # 帕姆展览馆第8弹 一部分 Wiki 顺序错位，具体而言
        # 1. 108011 本来在 11 位，被提前到了 9 位，108009 和 108010 顺序延后
        # 2. 108012 (12 位) 和 108013 (13 位) 错位
        108011: "08-09",  # 玲可-冲
        108012: "08-13",  # 艾丝妲-发红包
        108013: "08-12",  # 白露-吐泡泡
        # 帕姆展览馆第11弹 后大半部分 Wiki 顺序错位，具体而言：
        # 1. 111005 (5 位) 被移动到了 13 位
        # 2. 111006 (6 位) 被移动到了 16 位
        111005: "11-13",
        111006: "11-16",
        # 提前实装的表情，为了游戏内短信提前实装的表情包
        # 实装时仍不可用于玩家间短信，一般下个版本就可以了
        30008: "11-01",
        30009: "11-02",
        30010: "11-03",
        30011: "11-16",
        30012: "11-13",
        30013: "11-04",
        # 14 15 16 是花火发给玩家的短信中出现，见最顶上的隐藏款
        30017: "16-03",
        30018: "16-04",
        30021: "17-04",
        30024: "18-02",
        30025: "19-01",
        30026: "19-02",
        30027: "19-03",
        30028: "19-07",
        30029: "20-05",
        30030: "20-07",
        30031: "20-10",
        30032: "21-05",
        30033: "21-07",
        30034: "24-05",
    }

    @functools.cached_property
    def keywords(self) -> str:
        return self._game.text(self._excel.key_words)

    def wiki(self) -> str:  # noqa: PLR0911
        # 毫无办法，Wiki 上顺序是乱的，只能硬编码了
        # 除了玩家不可用的隐藏表情包之外，其它表情包均按照游戏内顺序在 match 中排序
        def wiki_id(group: int, order: int) -> str:
            return f"{group:02}-{order:02}"

        match self.id:
            case id_ if 107001 <= id_ <= 107007:
                # 107000 是第7弹
                assert self._excel.emoji_group_id is not None
                assert self._excel.same_group_order is not None
                return wiki_id(self._excel.emoji_group_id - 100, self._excel.same_group_order)
            case id_ if id_ in (108009, 108010):
                # 第8弹错位处理
                return wiki_id(id_ // 1000 - 100, id_ % 1000 + 1)
            case id_ if 111007 <= id_ <= 111014:
                # 第11弹错位处理
                return wiki_id(id_ // 1000 - 100, id_ % 1000 - 2)
            case id_ if id_ in (111015, 111016):
                # 第11弹错位处理
                return wiki_id(id_ // 1000 - 100, id_ % 1000 - 1)
            case id_ if 105000 <= id_ < 106000 or 108000 <= id_ < 111005 or 121000 <= id_ < 122000:
                # 105000 是第6弹
                # 108000 是第8弹
                # 109000 是第9弹
                # 110000 是第10弹
                # 111000 是第11弹
                # 121000 是第12弹
                assert self._excel.emoji_group_id is not None
                assert self._excel.same_group_order is not None
                return wiki_id(self._excel.emoji_group_id - 100, self._excel.same_group_order)
            # 从「帕姆展览馆第13弹」开始
            # 因为 Wiki 中间插入了一个不属于游戏的表情包系列（来自微信）
            # 因此需要 group_id 要从 -100 变成 -99 才是 Wiki 顺序
            case id_ if 114000 <= id_ < 125000 or 131000 <= id_ < 132000:
                # 131000 是第 13 弹，给我整不会了
                # 114000 是第 14 弹
                # 115000 是第 15 弹
                # 116000 是第 16 弹，出现了 id 序和 same_group_order 序不同的贴纸
                # 117000 是第 17 弹
                # 118000 是第 18 弹
                # 119000 是第 19 弹
                # 120000 是第 20 弹
                # 121000 是第 21 弹
                # 122000 是第 22 弹
                # 123000 是第 23 弹
                # 124000 是第 24 弹
                assert self._excel.emoji_group_id is not None
                assert self._excel.same_group_order is not None
                return wiki_id(self._excel.emoji_group_id - 99, self._excel.same_group_order)
            case id_:
                return self.__WIKI_MAPPING.get(id_) or " ".join(
                    f"""
                        表情未匹配 wiki
                        id: {self.id}, name: {self.keywords}
                        group: {self._excel.emoji_group_id}
                        order: {self._excel.same_group_order}
                        path: {self._excel.emoji_path}
                    """.split()
                )


class EmojiGroup(View[excel.EmojiGroup]):
    ExcelOutput: typing.Final = excel.EmojiGroup


class MessageContactsCamp(View[excel.MessageContactsCamp]):
    ExcelOutput: typing.Final = excel.MessageContactsCamp

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)


class MessageContactsConfig(View[excel.MessageContactsConfig]):
    ExcelOutput: typing.Final = excel.MessageContactsConfig

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @functools.cached_property
    def signature(self) -> str:
        return "" if self._excel.signature_text is None else self._game.text(self._excel.signature_text)

    @functools.cached_property
    def __camp(self) -> MessageContactsCamp | None:
        return (
            None if self._excel.contacts_camp is None else self._game.message_contacts_camp(self._excel.contacts_camp)
        )

    def camp(self) -> MessageContactsCamp | None:
        return None if self.__camp is None else MessageContactsCamp(self._game, self.__camp._excel)

    @functools.cached_property
    def __type(self) -> MessageContactsType | None:
        return (
            None if self._excel.contacts_type is None else self._game.message_contacts_type(self._excel.contacts_type)
        )

    def type(self) -> MessageContactsType | None:
        return None if self.__type is None else MessageContactsType(self._game, self.__type._excel)

    @functools.cached_property
    def __sections(self) -> list[MessageSectionConfig]:
        sections = [
            MessageSectionConfig(self._game, section)
            for section in self._game._message_contact_sections.get(self.id, ())  # pyright: ignore[reportPrivateUsage]
        ]
        sections.sort(key=lambda section: section.id)
        return sections

    def sections(self) -> collections.abc.Iterable[MessageSectionConfig]:
        return (MessageSectionConfig(self._game, section._excel) for section in self.__sections)

    @property
    def __formatter(self) -> Formatter:
        return self._game._mw_formatter  # pyright: ignore[reportPrivateUsage]

    def wiki(self) -> str:
        name = self.__formatter.format(self.name)
        wiki = io.StringIO()
        _ = wiki.write("{{#subobject:")
        _ = wiki.write(name)
        _ = wiki.write("-短信内容")
        _ = wiki.write("\n|@category=短信头像")
        _ = wiki.write("\n|名称=")
        _ = wiki.write(name)
        _ = wiki.write("\n|阵营=")
        _ = wiki.write("" if self.__camp is None else self.__camp.name)
        _ = wiki.write("\n|类型=")
        _ = wiki.write("" if self.__type is None else self.__type.name)
        _ = wiki.write("\n|头像= <!-- ")
        _ = wiki.write(self._excel.icon_path)
        _ = wiki.write(" -->")
        _ = wiki.write("\n}}")
        for section in self.__sections:
            _ = wiki.write("\n\n{{短信内容\n|人物=")
            _ = wiki.write(name)
            contacts_type = "" if self.__type is None else self.__type.name
            if contacts_type != "角色" and self.signature != "":
                _ = wiki.write("\n|签名=")
                _ = wiki.write(self.signature)
            _ = wiki.write("\n|短信标题=<!-- 填入相关事件或任务 -->")
            _ = wiki.write("\n|版本=<!-- 填入版本 -->")
            _ = wiki.write("\n|排序=<!-- 填入排序 -->")
            main_mission = section.main_mission()
            if main_mission is not None:
                _ = wiki.write("\n|接取任务=")
                _ = wiki.write(main_mission.name)
            else:
                _ = wiki.write("\n|任务链接=<!-- 填入任务名 -->")
                _ = wiki.write("\n|活动链接=<!-- 填入活动名 -->")
            _ = wiki.write("\n|内容=")
            section.wiki_iter_message(wiki, "\n  ", section, None)
            _ = wiki.write("\n}}")
        return wiki.getvalue()


class MessageContactsType(View[excel.MessageContactsType]):
    ExcelOutput: typing.Final = excel.MessageContactsType

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)


class MessageGroupConfig(View[excel.MessageGroupConfig]):
    ExcelOutput: typing.Final = excel.MessageGroupConfig


class MessageItemConfig(View[excel.MessageItemConfig]):
    ExcelOutput: typing.Final = excel.MessageItemConfig

    @property
    def id(self) -> int:
        return self._excel.id

    @property
    def section_id(self) -> int | None:
        return self._excel.section_id

    @functools.cached_property
    def __section(self) -> MessageSectionConfig | None:
        return None if self._excel.section_id is None else self._game.message_section_config(self._excel.section_id)

    def section(self) -> MessageSectionConfig | None:
        return None if self.__section is None else MessageSectionConfig(self._game, self.__section._excel)

    @functools.cached_property
    def main_text(self) -> str:
        return "" if self._excel.main_text is None else self._game.text(self._excel.main_text)

    @functools.cached_property
    def option_text(self) -> str:
        return "" if self._excel.option_text is None else self._game.text(self._excel.option_text)

    @property
    def type(self) -> message.ItemType:
        return self._excel.item_type

    @functools.cached_property
    def next_ids(self) -> tuple[int, ...]:
        return tuple(self._excel.next_item_id_list)

    @property
    def content_id(self) -> int | None:
        if self._excel.item_content_id is not None:
            return self._excel.item_content_id
        if self._excel.item_image_id is not None:
            return self._excel.item_image_id
        return None

    @property
    def __formatter(self) -> Formatter:
        return self._game._mw_formatter  # pyright: ignore[reportPrivateUsage]

    def __wiki_image(self, image_id: int) -> str:
        image = self._game.message_item_image(image_id)
        assert image is not None
        main_text = "" if self.main_text == "" else self.__formatter.format(self.main_text) + " "
        return (
            f"{main_text}<!-- Image: {image.image_path} -->"
            if image.female_image_path is None or image.female_image_path == ""
            else f"{main_text}<!-- Image: 穹 {image.image_path} 星 {image.female_image_path} -->"
        )

    @functools.cached_property
    def _contacts(self) -> MessageContactsConfig | None:
        return None if self._excel.contacts_id is None else self._game.message_contacts_config(self._excel.contacts_id)

    def contacts(self) -> MessageContactsConfig | None:
        return None if self._contacts is None else MessageContactsConfig(self._game, self._contacts._excel)

    def wiki_sticker(self) -> EmojiConfig | None:
        if self.content_id is None:
            return None
        emoji = self._game.emoji_config(self.content_id)
        if emoji is not None:
            return emoji
        # 1.2 版本及之前没有解包 emoji 信息，尝试一下手动组装
        # 因为没有 group 因此出错会 panic
        model = excel.EmojiConfig(
            emoji_id=self.content_id,
            gender=message.EmojiGender.All,
            emoji_group_id=None,
            key_words="",
            emoji_path="",
            same_group_order=None,
            gender_link=None,
            is_train_members=False,
        )
        return EmojiConfig(self._game, model)

    def wiki_type(self) -> str:
        match self.type:
            case message.ItemType.Image | message.ItemType.Link | message.ItemType.Raid | message.ItemType.Video:
                return "图片"
            case message.ItemType.Sticker:
                return "表情"
            case message.ItemType.Text:
                return "文本" if self.content_id is None else "图片"

    def wiki_main_text(self) -> str:
        match self.type:
            case message.ItemType.Image:
                assert self.content_id is not None
                text = self.__wiki_image(self.content_id)
            case message.ItemType.Link:
                assert self.content_id is not None
                link = self._game.message_item_link(self.content_id)
                assert link is not None
                text = f"<!-- Link: {link.image_path} -->"
            case message.ItemType.Raid:
                return "<!-- Raid -->"
                # print(self._excel)
                # assert self.content_id is not None
                # raid = self._game.message_item_raid_entrance(self.content_id)
                # assert raid is not None
                # text = f"<!-- Raid: {raid.image_path} -->"
            case message.ItemType.Sticker:
                assert self.content_id is not None
                sticker = self.wiki_sticker()
                assert sticker is not None
                text = sticker.wiki()
            case message.ItemType.Text:
                text = (
                    self.__formatter.format(self.main_text)
                    if self.content_id is None
                    else self.__wiki_image(self.content_id)  # 1.2 及之前 image 的 type 也是 Text
                )
            case message.ItemType.Video:
                assert self.content_id is not None
                video = self._game.message_item_video(self.content_id)
                assert video is not None
                text = f"<!-- Video: {video.image_path} -->"
        return text


class MessageItemImage(View[excel.MessageItemImage]):
    ExcelOutput: typing.Final = excel.MessageItemImage

    @property
    def image_path(self) -> str:
        return self._excel.image_path

    @property
    def female_image_path(self) -> str | None:
        return self._excel.female_image_path

    def wiki(self) -> str:
        return (
            f"<!-- {self._excel.image_path} -->"
            if self._excel.female_image_path is None
            else f"<!-- 穹: {self._excel.image_path} 星: {self._excel.female_image_path} -->"
        )


class MessageItemLink(View[excel.MessageItemLink]):
    ExcelOutput: typing.Final = excel.MessageItemLink

    @property
    def image_path(self) -> str:
        return self._excel.image_path


class MessageItemRaidEntrance(View[excel.MessageItemRaidEntrance]):
    ExcelOutput: typing.Final = excel.MessageItemRaidEntrance

    @property
    def image_path(self) -> str:
        return self._excel.image_path


class MessageItemVideo(View[excel.MessageItemVideo]):
    ExcelOutput: typing.Final = excel.MessageItemVideo

    @property
    def image_path(self) -> str:
        return self._excel.image_path


class _Node(metaclass=abc.ABCMeta):
    """消息节点，可能是起点 MessageSectionConfig 或任意节点 _Message"""

    def __init__(self):
        self.confluence: MessageItemConfig | _Uninit | None = _uninit

    @property
    @abc.abstractmethod
    def id(self) -> int: ...  # 用于调试，倒是可以删，不过还是放着吧

    @property
    @abc.abstractmethod
    def _option_half(self) -> bool:
        """表示本 _Node 是用来处理 MainText 还是处理 NextItemIDList 的"""

    @functools.cached_property
    @abc.abstractmethod
    def _successors(self) -> tuple[_Message, ...]:
        """
        后继需要处理的节点
        对于 option_half 的节点就是 NextItemIDList 指向的 _Node, 且后继 _option_half 都是 False
        对于 main_text_half 的节点的后继那就是 _option_half == True 的同一个对象
        """


class _Uninit: ...


_uninit = _Uninit()


class _Message(MessageItemConfig, _Node):  # pyright: ignore[reportUnsafeMultipleInheritance]
    # 反正是非导出对象，这里就搞一堆后置初始化了
    # message_dict 和 neighbour 是需要由 MessageSectionConfig 初始化
    # 这是因为这些数据上挂了 functools，为了避免对同一条消息反反复复计算文案和后置所以都放到一起
    def __init__(self, game: GameData, message: excel.MessageItemConfig, is_option: bool = False):
        MessageItemConfig.__init__(self, game, message)
        _Node.__init__(self)
        self.__is_option = is_option
        """self 表示选项还是正文"""
        self.message_dict: dict[int, _Message] = {}  # 依赖外部手动初始化
        """所有同 section 的 message"""
        self.neighbour: _Message | None = None  # 依赖外部手动初始化
        """neighbour 表示当自己不是 option_half 时候的后继"""

    @functools.cached_property
    def _successors(self) -> tuple[_Message, ...]:
        if len(self._excel.next_item_id_list) == 0:
            return ()
        # 后继有 0 个的情况不可能有 _option_half
        if self._option_half:
            return tuple(self.message_dict[id] for id in self._excel.next_item_id_list)
        if self.neighbour is not None:
            return (self.neighbour,)
        # 这里 next_item_id_list 只可能有一项
        assert len(self._excel.next_item_id_list) == 1
        return (self.message_dict[self._excel.next_item_id_list[0]],)

    @property
    @typing_extensions.override
    def _option_half(self) -> bool:
        return self.__is_option

    def shallow_eq(self, other: _Message) -> bool:  # noqa: PLR0911
        """
        当自身数据一样时，判断为相等
        需要注意的是，对于选项来说，它的「自身」是包含 NextItem 的 OptionText 的，也就是我们要多找一层
        """
        if self is other:
            return True
        if self._game is not other._game:
            return False
        if self._excel is other._excel or self._excel.id_ == other._excel.id_:
            return True
        if self._option_half:
            # 是 option 的情况只需要判断后继们的 OptionText 是否相等
            this_options = [message.option_text for message in self._successors]
            that_options = [message.option_text for message in other._successors]
            return this_options == that_options
        this_contacts = None if self._contacts is None else self._contacts.name
        that_contacts = None if other._contacts is None else other._contacts.name
        return (
            this_contacts == that_contacts and self.content_id == other.content_id and self.main_text == other.main_text
        )

    @typing_extensions.override
    def __eq__(self, other: object) -> bool:
        """
        当且仅当所有自身和所有后继都相等时，才判断为相等
        需要注意的是最后一步判断后继是否相等存在递归，可能会导致性能劣化。
        目前经测试影响不大，可能是提前用 ID 判等跳出的数据比较多，也就是 ID 不同内容相同的极端数据比较少
        """
        if not isinstance(other, _Message):
            return False
        if self is other:
            return True
        if self._option_half != other._option_half:
            return False
        if self._excel is other._excel or self._excel.id_ == other._excel.id_:
            return True  # 因为上面已经过滤了选择和非选择不一样的情况，所以这里肯定是 True
        if not self.shallow_eq(other):
            return False
        return self._successors == other._successors

    @functools.cached_property
    def __hash_cache(self) -> int:
        """
        计算并缓存 hash 值
        需要注意的是最后一项包含了后继 hash 会导致递归，所以需要缓存
        没有缓存会导致性能劣化，目前看全部短信算一次加起来总共从 3s 劣化到 5s 左右
        """
        if self._option_half:
            return hash((*(message.option_text for message in self._successors), *self._successors))
        contacts_name = "" if self._contacts is None else self._contacts.name
        return hash((contacts_name, self.content_id, self.main_text, *self._successors))

    @typing_extensions.override
    def __hash__(self) -> int:
        return self.__hash_cache


class MessageSectionConfig(View[excel.MessageSectionConfig], _Node):  # pyright: ignore[reportUnsafeMultipleInheritance]
    ExcelOutput: typing.Final = excel.MessageSectionConfig

    def __init__(self, game: GameData, excel: excel.MessageSectionConfig):
        View.__init__(self, game, excel)  # pyright: ignore[reportUnknownMemberType]
        _Node.__init__(self)

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def __contacts(self) -> MessageContactsConfig:
        return MessageContactsConfig(self._game, self._game._message_section_contacts[self.id])  # pyright: ignore[reportPrivateUsage]

    def contacts(self) -> MessageContactsConfig:
        return MessageContactsConfig(self._game, self.__contacts._excel)

    @property
    @typing_extensions.override
    def _option_half(self) -> bool:
        return True  # MessageSection 不会有正文，总是要找后继，所以这里 option_half 只能是 True

    @functools.cached_property
    def _successors(self) -> tuple[_Message, ...]:
        return tuple(self.__message_dict[id] for id in self._excel.start_message_item_id_list)

    def __find_confluence(self, current: _Node) -> _Message | None:
        """找到公共后继，主要为了找到选项终点合并后续重复项"""
        if current.confluence is not _uninit:
            return current.confluence  # pyright: ignore[reportReturnType]
        if len(current._successors) == 0:
            current.confluence = None
            return current.confluence
        if len(current._successors) == 1:
            current.confluence = current._successors[0]
            return current.confluence  # 还是可能有没设置的，比如 MessageSectionConfig
        queue: list[_Message | None] = list(current._successors)
        visit: dict[_Message, int] = collections.defaultdict(int)
        while any(node is not None for node in queue):
            for index, node in enumerate(queue):
                if node is None:
                    # 某条分支已经迭代到整个对话列表最后一句了，这条分支不继续找了
                    # 但是有可能另一分支速度较慢，仍未到聚合点，所以需要继续迭代找完为止
                    continue
                next_node = self.__find_confluence(node)
                queue[index] = next_node
                if next_node is None:
                    continue
                visit[next_node] += 1
                if visit[next_node] == len(queue):
                    current.confluence = next_node
                    return current.confluence
        current.confluence = None
        return current.confluence

    @property
    def __formatter(self) -> Formatter:
        return self._game._mw_formatter  # pyright: ignore[reportPrivateUsage]

    @staticmethod
    def __wiki_dialogue(
        wiki: typing.IO[str], direction: typing.Literal["左", "右"], contacts_name: str, item: MessageItemConfig
    ):
        _ = wiki.write("{{角色对话|")
        _ = wiki.write(direction)
        _ = wiki.write("|")
        _ = wiki.write(contacts_name)
        _ = wiki.write("|")
        _ = wiki.write(item.wiki_type())
        _ = wiki.write("|")
        _ = wiki.write(item.wiki_main_text())
        _ = wiki.write("}}")

    def __wiki_write_message_select(self, wiki: typing.IO[str], indent: str, node: _Node, confluence: _Message | None):
        """
        处理需要玩家选择的选项（分支）消息
        本函数会直接写入这条选项分支开的后续剧情
        直到所有分支重新汇合为止

        参数 item 是分支开始的选项消息，confluence 是若本选项外面还套着一层选项，则传入外层选项的聚合节点
        """
        if len(node._successors) == 1 and node._successors[0]._excel.option_text is None:
            return  # 应该只有 MessageSectionConfig 进来的时候会直接从这里返回
        _ = wiki.write(indent)
        _ = wiki.write("{{短信选项")
        is_sticker = all(item.type is message.ItemType.Sticker for item in node._successors)
        if is_sticker:
            _ = wiki.write("|表情")
        if len(node._successors) == 1:
            indent = ""  # 假选项
        next_indent = indent + "  "
        for index, next_node in enumerate(node._successors):
            _ = wiki.write(indent)
            _ = wiki.write(f"|选项{index + 1}=")
            if is_sticker:
                sticker = next_node.wiki_sticker()
                assert sticker is not None
                _ = wiki.write(sticker.wiki())
            else:
                _ = wiki.write(self.__formatter.format(next_node.option_text))
            if next_node != confluence:
                _ = wiki.write(indent)
                _ = wiki.write(f"|剧情{index + 1}=")
                self.wiki_iter_message(wiki, next_indent, next_node, confluence)
        _ = wiki.write(indent)
        _ = wiki.write("}}")

    def __wiki_write_message_single(self, wiki: typing.IO[str], indent: str, item: _Message):
        """处理当前消息非选项部分的情况"""
        contacts_name = ""
        _ = wiki.write(indent)
        match item._excel.sender:
            case message.Sender.NPC:
                contacts = item.contacts() or self.contacts()
                contacts_name = self.__formatter.format(contacts.name)
                self.__wiki_dialogue(wiki, "左", contacts_name, item)
            case message.Sender.Player | message.Sender.PlayerAuto:
                contacts = item.contacts()
                contacts_name = "开拓者" if contacts is None else self.__formatter.format(contacts.name)
                self.__wiki_dialogue(wiki, "右", contacts_name, item)
            case message.Sender.System:
                _ = wiki.write("{{短信警告|")
                _ = wiki.write(self.__formatter.format(item.main_text))
                _ = wiki.write("}}")

    def wiki_iter_message(self, wiki: typing.IO[str], indent: str, node: _Node, confluence: _Message | None):
        """
        用于生成完整短信内容
        逻辑比较复杂，原因在于数据结构不够解耦，选项和正文是耦合在一起的
        """
        if node == confluence:
            return
        next_confluence = self.__find_confluence(node)
        if node._option_half:
            self.__wiki_write_message_select(wiki, indent, node, next_confluence)
        else:
            assert isinstance(node, _Message)
            self.__wiki_write_message_single(wiki, indent, node)
        if next_confluence is not None:
            self.wiki_iter_message(wiki, indent, next_confluence, confluence)

    @functools.cached_property
    def __main_mission(self) -> MainMission | None:
        return None if self._excel.main_mission_link is None else self._game.main_mission(self._excel.main_mission_link)

    def main_mission(self) -> MainMission | None:
        from .mission import MainMission

        return None if self.__main_mission is None else MainMission(self._game, self.__main_mission._excel)

    @functools.cached_property
    def __message_dict(self) -> dict[int, _Message]:
        # 逻辑是这样的
        # 进入 wiki_iter_message 之后，立刻就会执行 self.__find_confluence(self)
        # 找 confluence 的时候会找 self 的 _successors，这里就会调用这个 self.__message_dict
        # 于是所有 _Message 就被初始化了
        items = self._game._message_section_config_items[self._excel.id_]  # pyright: ignore[reportPrivateUsage]
        message_dict: dict[int, _Message] = {}
        messages: list[_Message] = []
        for item in items:
            # 用缩写是因为 message 被包名占了，用不了……
            msg = _Message(self._game, item)
            message_dict[msg.id] = msg
            messages.append(msg)
        for msg in messages:
            msg.message_dict = message_dict
            if len(msg._excel.next_item_id_list) == 0:
                continue
            if len(msg._excel.next_item_id_list) > 1:
                option_message = _Message(self._game, msg._excel, True)
                msg.neighbour = option_message
                option_message.message_dict = message_dict
            else:  # 存在只有一个选项的假选择，需要判断后继的 OptionText 是否非空
                next_message = message_dict.get(msg._excel.next_item_id_list[0])
                if next_message is not None and next_message._excel.option_text is not None:
                    option_message = _Message(self._game, msg._excel, True)
                    msg.neighbour = option_message
                    option_message.message_dict = message_dict

        return message_dict

    def wiki(self) -> str:
        wiki = io.StringIO()
        _ = wiki.write("{{角色对话|模板开始|")
        _ = wiki.write(self.__contacts.name)
        contacts_type = self.__contacts.type()
        contacts_type = "" if contacts_type is None else contacts_type.name
        if contacts_type != "角色" and self.__contacts.signature != "":
            _ = wiki.write("|")
            _ = wiki.write(self.__contacts.signature)
        _ = wiki.write("}}")
        self.wiki_iter_message(wiki, "\n  ", self, None)
        if self.__main_mission is not None:
            _ = wiki.write("\n  {{接取任务|")
            _ = wiki.write(str(self.__main_mission.type))
            _ = wiki.write("|")
            _ = wiki.write(self.__main_mission.name)
            _ = wiki.write("}}")
        _ = wiki.write("\n{{角色对话|模板结束}}")
        return wiki.getvalue()
