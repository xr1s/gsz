from __future__ import annotations
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
            case id_ if 114000 <= id_ < 121000 or 131000 <= id_ < 132000:
                # 131000 是第 13 弹，给我整不会了
                # 114000 是第 14 弹
                # 115000 是第 15 弹
                # 116000 是第 16 弹，出现了 id 序和 same_group_order 序不同的贴纸
                # 117000 是第 17 弹
                # 118000 是第 18 弹
                # 119000 是第 19 弹
                # 120000 是第 20 弹
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
        return [
            MessageSectionConfig(self._game, section)
            for section in self._game._message_contact_sections.get(self.id, ())  # pyright: ignore[reportPrivateUsage]
        ]

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
            _ = wiki.write("\n|短信标题=<!-- 填入相关事件或任务 -->")
            _ = wiki.write("\n|版本=<!-- 填入版本 -->")
            contacts_type = "" if self.__type is None else self.__type.name
            if contacts_type != "角色" and self.signature != "":
                _ = wiki.write("\n|签名=")
                _ = wiki.write(self.signature)
            main_mission = section.main_mission()
            if main_mission is not None:
                _ = wiki.write("\n|接取任务=")
                _ = wiki.write(main_mission.name)
            else:
                _ = wiki.write("\n|任务链接=<!-- 填入任务名 -->")
                _ = wiki.write("\n|活动链接=<!-- 填入活动名 -->")
            _ = wiki.write("\n|内容=")
            section.wiki_message_content(wiki, "\n  ")
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

    @typing_extensions.override
    def __init__(self, game: GameData, excel: excel.MessageItemConfig):
        super().__init__(game, excel)
        self.__confluence: MessageItemConfig | None = None

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

    @property
    def confluence(self) -> MessageItemConfig | None:
        return self.__confluence

    @confluence.setter
    def confluence(self, confluence: MessageItemConfig):
        self.__confluence = confluence

    def nexts(self) -> list[int]:
        return self._excel.next_item_id_list

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
    def __contacts(self) -> MessageContactsConfig | None:
        return None if self._excel.contacts_id is None else self._game.message_contacts_config(self._excel.contacts_id)

    def contacts(self) -> MessageContactsConfig | None:
        return None if self.__contacts is None else MessageContactsConfig(self._game, self.__contacts._excel)

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
            key_words=excel.Text(hash=0),
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


class Node(typing.Protocol):
    """
    消息节点，可能是起点 MessageSectionConfig 或任意节点 MessageItemConfig
    """

    @property
    def confluence(self) -> MessageItemConfig | None: ...
    @confluence.setter
    def confluence(self, confluence: MessageItemConfig): ...
    def nexts(self) -> list[int]: ...


class MessageSectionConfig(View[excel.MessageSectionConfig]):
    ExcelOutput: typing.Final = excel.MessageSectionConfig

    def __init__(self, game: GameData, excel: excel.MessageSectionConfig):
        super().__init__(game, excel)
        self.__confluence: MessageItemConfig | None = None

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def __items(self) -> list[MessageItemConfig]:
        items = self._game._message_section_config_items[self._excel.id]  # pyright: ignore[reportPrivateUsage]
        return [MessageItemConfig(self._game, item) for item in items]

    @functools.cached_property
    def __contacts(self) -> MessageContactsConfig:
        return MessageContactsConfig(self._game, self._game._message_section_contacts[self.id])  # pyright: ignore[reportPrivateUsage]

    def contacts(self) -> MessageContactsConfig:
        return MessageContactsConfig(self._game, self.__contacts._excel)

    @functools.cached_property
    def __item_dict(self) -> dict[int, MessageItemConfig]:
        return {item.id: item for item in self.__items}

    @property
    def confluence(self) -> MessageItemConfig | None:
        return self.__confluence

    @confluence.setter
    def confluence(self, confluence: MessageItemConfig):
        self.__confluence = confluence

    def nexts(self) -> list[int]:
        return self._excel.start_message_item_id_list

    def find_common_confluence(self, current: Node) -> MessageItemConfig | None:
        """找到公共后继，主要为了处理选项"""
        if current.confluence is not None:
            return current.confluence  # 记忆化
        if len(current.nexts()) == 0:
            return None
        if len(current.nexts()) == 1:
            current.confluence = self.__item_dict[current.nexts()[0]]
            return current.confluence
        queue: list[MessageItemConfig | None] = [self.__item_dict[k] for k in current.nexts()]
        visit: dict[int, int] = collections.defaultdict(int)
        while any(node is not None for node in queue):
            for index, node in enumerate(queue):
                if node is None:
                    # 某条分支已经迭代到整个对话列表最后一句了，这条分支不继续找了
                    # 但是有可能另一分支速度较慢，仍未到聚合点，所以需要继续迭代找完为止
                    continue
                next_node = self.find_common_confluence(node)
                queue[index] = next_node
                if next_node is None:
                    continue
                visit[next_node.id] += 1
                if visit[next_node.id] == len(current.nexts()):
                    current.confluence = next_node
                    return current.confluence
        return None

    @property
    def __formatter(self) -> Formatter:
        return self._game._mw_formatter  # pyright: ignore[reportPrivateUsage]

    @staticmethod
    def __wiki_dialogue(
        wiki: io.StringIO,
        direction: typing.Literal["左", "右"],
        contacts_name: str,
        item: MessageItemConfig,
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

    def __wiki_write_message_item(self, wiki: io.StringIO, indent: str, item: MessageItemConfig):
        """
        处理单条非选项（分支）消息，参数 item 就是消息本身

        主要逻辑复杂在于判断消息类型（文字、图片、表情包）、发送者接收者真实账号
        """

        contacts_name = ""
        _ = wiki.write(indent)
        match item._excel.sender:
            case message.Sender.NPC:
                contacts = item.contacts()
                if contacts is None:
                    contacts = self.__contacts
                contacts_name = contacts.name
                if contacts_name == "{NICKNAME}":
                    contacts_name = "开拓者"
                self.__wiki_dialogue(wiki, "左", contacts_name, item)
            case message.Sender.Player | message.Sender.PlayerAuto:
                contacts = item.contacts()
                contacts_name = "开拓者" if contacts is None else contacts.name
                self.__wiki_dialogue(wiki, "右", contacts_name, item)
            case message.Sender.System:
                _ = wiki.write("{{短信警告|")
                _ = wiki.write(self.__formatter.format(item.main_text))
                _ = wiki.write("}}")

    def __wiki_iter_message_select(
        self, wiki: io.StringIO, indent: str, item: Node, confluence: MessageItemConfig | None
    ):
        """
        处理需要玩家选择的选项（分支）消息
        本函数会直接写入这条选项分支开的后续剧情
        直到所有分支重新汇合为止

        参数 item 是分支开始的选项消息，confluence 是若本选项外面还套着一层选项，则传入外层选项的聚合节点
        """
        # 存在分支选项为表情的情况，需要在聊天记录中再手动发一条表情
        _ = wiki.write(indent)
        _ = wiki.write("{{短信选项")
        nexts = [self.__item_dict[k] for k in item.nexts()]
        is_sticker = all(item.type == message.ItemType.Sticker for item in nexts)
        if is_sticker:
            _ = wiki.write("|表情")
        next_confluence = self.find_common_confluence(item)
        for index, next_item in enumerate(nexts):
            _ = wiki.write(indent)
            _ = wiki.write(f"|选项{index + 1}=")
            if is_sticker:
                sticker = next_item.wiki_sticker()
                assert sticker is not None
                _ = wiki.write(sticker.wiki())
            else:
                _ = wiki.write(self.__formatter.format(next_item.option_text))
            _ = wiki.write(indent)
            _ = wiki.write(f"|剧情{index + 1}=")
            self.__wiki_iter_message_single(wiki, indent + "  ", next_item, next_confluence, False)
        _ = wiki.write(indent)
        _ = wiki.write("}}")
        if next_confluence is not None:
            self.__wiki_iter_message_single(wiki, indent, next_confluence, confluence, True)

    def __wiki_iter_message_single(
        self,
        wiki: io.StringIO,
        indent: str,
        item: MessageItemConfig,
        confluence: MessageItemConfig | None,
        single_child: bool,
    ):
        """
        处理当前消息非选项的情况
        虽然参数差不多，不过不像和当前消息是选项的情况合并，主要是因为处理逻辑大相径庭

        参数 item 是分支开始的选项消息，confluence 是若外面套着一层选项，则传入外层选项的聚合节点
        """
        if confluence is not None and item.id == confluence.id:
            return
        if single_child and item.option_text != "":
            # 假分支，有选项但是无分支
            # 只有在父节点只有自己一个后继的时候才会进入本函数
            _ = wiki.write(indent)
            _ = wiki.write("{{短信选项")
            # item.type 可能为 Sticker，但我看了几个选项都是文字的，因此应该无视即可
            _ = wiki.write("|选项1=")
            _ = wiki.write(self.__formatter.format(item.option_text))
            _ = wiki.write("}}")
        self.__wiki_write_message_item(wiki, indent, item)
        # nexts = item.nexts()
        nexts = [self.__item_dict[k] for k in item.nexts()]
        if len(nexts) == 0:
            return
        if len(nexts) > 1:
            self.__wiki_iter_message_select(wiki, indent, item, confluence)
            return
        self.__wiki_iter_message_single(wiki, indent, nexts[0], confluence, True)

    def wiki_message_content(self, wiki: io.StringIO, indent: str):
        """
        生成 BWIKI 的短信模板，不包含开头和结尾的 {{短信内容|}} 或者 {{角色对话|}}
        {{短信内容|}} 由 MessageSectionConfig 的 wiki() 方法补充
        {{角色对话|}} 由 MessageContactsConfig 的 wiki() 方法补充
        """
        if len(self._excel.start_message_item_id_list) == 1:
            self.__wiki_iter_message_single(wiki, indent, self.__item_dict[self.nexts()[0]], None, True)
            return
        self.__wiki_iter_message_select(wiki, indent, self, None)

    @functools.cached_property
    def __main_mission(self) -> MainMission | None:
        return None if self._excel.main_mission_link is None else self._game.main_mission(self._excel.main_mission_link)

    def main_mission(self) -> MainMission | None:
        from .mission import MainMission

        return None if self.__main_mission is None else MainMission(self._game, self.__main_mission._excel)

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
        self.wiki_message_content(wiki, "\n  ")
        if self.__main_mission is not None:
            _ = wiki.write("\n  {{接取任务|")
            _ = wiki.write(str(self.__main_mission.type))
            _ = wiki.write("|")
            _ = wiki.write(self.__main_mission.name)
            _ = wiki.write("}}")
        _ = wiki.write("\n{{角色对话|模板结束}}")
        return wiki.getvalue()
