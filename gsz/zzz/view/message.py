from __future__ import annotations

import collections.abc
import functools
import io
import typing

import typing_extensions

from .. import filecfg
from ..filecfg import message
from .base import View

if typing.TYPE_CHECKING:
    from ..data import GameData
    from .partner import PartnerConfig
    from .quest import QuestConfig


class DirectoryConfig(View[filecfg.DirectoryConfig]):
    FileCfg: typing.Final = filecfg.DirectoryConfig

    @functools.cached_property
    def __partner(self) -> PartnerConfig:
        partner = self._game.partner_config(self._filecfg.partner_id)
        assert partner is not None
        return partner

    def partner(self) -> PartnerConfig:
        from .partner import PartnerConfig

        return PartnerConfig(self._game, self.__partner._filecfg)


class MessageConfig(View[filecfg.MessageConfig]):
    FileCfg: typing.Final = filecfg.MessageConfig

    @property
    def id(self) -> int:
        return self._filecfg.id_

    @functools.cached_property
    def text(self) -> str | None:
        """文本消息，保证有文本时无选项，有选项时无文本"""
        return self._game.text(self._filecfg.text) if self._filecfg.text != "" else None

    @functools.cached_property
    def image(self) -> str | None:
        """文本消息，保证有文本时无选项，有选项时无文本"""
        return self._filecfg.image if self._filecfg.image != "" else None

    @functools.cached_property
    def voice(self) -> str | None:
        return self._filecfg.voice if self._filecfg.voice != "" else None

    @property
    def segment(self) -> int:
        return self._filecfg.segment

    @functools.cached_property
    def option_1(self) -> str | None:
        return self._game.text(self._filecfg.option_1) if self._filecfg.option_1 != "" else None

    @functools.cached_property
    def option_2(self) -> str | None:
        return self._game.text(self._filecfg.option_2) if self._filecfg.option_2 != "" else None

    @functools.cached_property
    def option_long_1(self) -> str | None:
        """选择对应选项后实际回复的消息正文，可能和选项本身文本相同"""
        return self._game.text(self._filecfg.option_long_1) if self._filecfg.option_long_1 != "" else None

    @functools.cached_property
    def option_long_2(self) -> str | None:
        """选择对应选项后实际回复的消息正文，可能和选项本身文本相同"""
        return self._game.text(self._filecfg.option_long_2) if self._filecfg.option_long_2 != "" else None

    @functools.cached_property
    def option_successor_1(self) -> int | None:
        return self._filecfg.option_successor_1 if self._filecfg.option_successor_1 != 0 else None

    @functools.cached_property
    def option_successor_2(self) -> int | None:
        return self._filecfg.option_successor_2 if self._filecfg.option_successor_2 != 0 else None

    @functools.cached_property
    def __directory(self) -> DirectoryConfig | None:
        return self._game.directory_config(self._filecfg.sender_id)

    def directory(self) -> DirectoryConfig | None:
        """自机角色特有的短信联系人页面，包含一些角色性格的备忘录"""
        return DirectoryConfig(self._game, self.__directory._filecfg) if self.__directory is not None else None

    @functools.cached_property
    def __npc(self) -> MessageNPC | None:
        return self._game.message_npc(self._filecfg.sender_id)

    @functools.cached_property
    def sender_name(self) -> str | None:
        if self._filecfg.sender_id == 0:
            return None
        if self._filecfg.sender_id == 998:
            return "匿名"
        if self._filecfg.sender_id == 999:
            return "兄妹"
        return self.__npc.name if self.__npc is not None else None

    @functools.cached_property
    def sender_icon(self) -> str | None:
        if self._filecfg.sender_id == 0:
            return None
        if self._filecfg.sender_id == 998:
            return "匿名"
        if self._filecfg.sender_id == 999:
            return "兄妹"
        return self.__npc.icon if self.__npc is not None else None


class _Uninit: ...


_uninit = _Uninit()


class _Message(MessageConfig):
    """将选项和内容拆成两条 Message 以方便寻找公共后继"""

    # 反正是非导出对象，这里就搞一堆后置初始化了
    # group 和 neighbours 是需要由 MessageGroupConfig 初始化
    # 这是因为这些数据上挂了 functools，为了避免对同一条消息反反复复计算文案和后置所以都放到一起
    def __init__(self, game: GameData, message: filecfg.MessageConfig, option_index: int | None = None):
        super().__init__(game, message)
        self.confluence: _Message | _Uninit | None = _uninit
        self.option_index: int = option_index or 0
        self.group: collections.abc.Sequence[_Message] = ()  # 依赖外部手动初始化
        self.neighbours: tuple[_Message, ...] | None = None
        """如果是选项根则非空，表示的是选项根的后继，由外部初始化"""

    @property
    def is_option(self) -> bool:
        return self._filecfg.type is message.Type.Option or self._filecfg.type is message.Type.ImageOption

    @property
    def is_option_root(self) -> bool:
        return self.is_option and self.option_index == 0

    @functools.cached_property
    def successors(self) -> tuple[_Message, ...]:
        if self.is_option_root:
            assert self.neighbours is not None
            return self.neighbours
        successor: _Message | None = None
        if not self.is_option and self._filecfg.successor == 0:
            # 非选项且 successor == 0 的情况，就是找同一个 segment 更后一条 Message
            segment = [message for message in self.group if message.segment == self.segment]
            index = next(k for k, msg in enumerate(segment) if msg._filecfg.id_ == self._filecfg.id_)
            successor = segment[index + 1] if index < len(segment) - 1 else None
        else:
            successors = (self._filecfg.successor, self._filecfg.option_successor_1, self._filecfg.option_successor_2)
            successor_segment = successors[self.option_index]
            if successor_segment != 0:
                # 仍然有可能为空，也许是测试数据
                successor = next((message for message in self.group if successor_segment == message.segment), None)
        return (successor,) if successor is not None else ()

    @functools.cached_property
    @typing_extensions.override
    def text(self) -> str | None:
        if self.is_option_root:
            return None
        this = super()
        texts = (this.text, this.option_long_1 or this.option_1, this.option_long_2 or this.option_2)
        return texts[self.option_index]

    def shallow_eq(self, other: _Message) -> bool:  # noqa: PLR0911
        """判断自身是否相同，比如是否均为选项根，是否文案相同"""
        if self is other:
            return True  # 同对象
        if self._game is not other._game:
            return False
        if self._filecfg.group_id != other._filecfg.group_id:
            return False  # 排除两个不在同一系列短信中的情况
        if self.is_option_root != other.is_option_root:
            return False  # 排除一个是选项根，一个是正文的情况
        if self._filecfg is other._filecfg or self._filecfg.id_ == other._filecfg.id_:
            # 如果是同一个对象，看看是不是指向同一句话
            # 就是在是选项的情况下，检查是不是都是开始或者都是同一个分支
            # 如果是正文，那同一个对象肯定相等
            if self.option_index == other.option_index:
                return True
            # 更上面排除了一个是选项根，一个是分支的情况
            # 这里排除了两个相等的情况，包含了两个都是选项根的情况、两个都是正文、两个都是分支但同一个分支的情况
            # 因此这里只有一种情况，就是两者均为选项分支，且不是同一个分支
            return self.text == other.text
        if self.is_option_root:  # 都是选项根，比较两个选项是否相等，不比较后续文案
            return self.option_1 == other.option_1 and self.option_2 == other.option_2
        if not self.is_option and (self.sender_name != other.sender_name or self.sender_icon != other.sender_icon):
            return False
        return self.text == other.text  # 都是正文，直接比较文案

    @typing_extensions.override
    def __eq__(self, other: object) -> bool:  # noqa: PLR0911
        """不仅要求自身相同，也要求后继相同"""
        if self is other:
            return True
        if not isinstance(other, _Message):
            return False
        if self._game is not other._game:
            return False
        if not self.shallow_eq(other):
            return False  # 自身不同
        # shallow_eq 中已经过滤了一个是选项根、一个非选项根的情况
        # 于是可以避免这种情况：self 是选项且只有一个后继，other 是正文，且他们后继相同
        return self.successors == other.successors

    @functools.cached_property
    def __hash_cache(self) -> int:
        if self.is_option_root and self._filecfg.option_2 == "":
            return hash((self.option_1, self.successors[0]))
        if self.is_option_root:
            return hash((self.option_1, self.option_2, self.successors[0], self.successors[1]))
        if self.is_option:
            return hash((self.text, *self.successors))  # 选项肯定是自己发送的，所以这里不用加 sender
        # successor 可能为空，所以用 * 解包
        return hash((self.sender_name, self.sender_icon, self.text, *self.successors))

    @typing_extensions.override
    def __hash__(self):
        return self.__hash_cache


class MessageGroupConfig(View[filecfg.MessageGroupConfig]):
    FileCfg: typing.Final = filecfg.MessageGroupConfig

    @property
    def id(self) -> int:
        return self._filecfg.id

    @functools.cached_property
    def __directory(self) -> DirectoryConfig | None:
        return self._game.directory_config(self._filecfg.contact_id)

    def directory(self) -> DirectoryConfig | None:
        return None if self.__directory is None else DirectoryConfig(self._game, self.__directory._filecfg)

    @functools.cached_property
    def __npc(self) -> MessageNPC | None:
        return self._game.message_npc(self._filecfg.contact_id)

    @functools.cached_property
    def contact_name(self) -> str:
        contact = self.__directory.partner() if self.__directory is not None else self.__npc
        assert contact is not None
        return contact.name

    @functools.cached_property
    def __messages(self) -> list[_Message]:
        messages: list[_Message] = []
        for msg in self._game._messages_of_group.get(self._filecfg.id, ()):  # pyright: ignore[reportPrivateUsage]
            node = _Message(self._game, msg)
            neighbours: list[_Message] = []
            if msg.option_1 != "":
                neighbours.append(_Message(self._game, msg, 1))
            if msg.option_2 != "":
                neighbours.append(_Message(self._game, msg, 2))
            node.neighbours = tuple(neighbours)
            messages.append(node)
        for msg in messages:
            msg.group = messages
        return messages

    __MISSING_QUEST = {1203550109, 12080101, 12080102, 1300301210, 1303013135}

    @functools.cached_property
    def __quests(self) -> list[QuestConfig]:
        return list(
            self._game.quest_config(
                quest_id for quest_id in self._filecfg.quest_ids if quest_id not in self.__MISSING_QUEST
            )
        )

    def quests(self) -> collections.abc.Iterable[QuestConfig]:
        from .quest import QuestConfig

        return (QuestConfig(self._game, quest._filecfg) for quest in self.__quests)

    @functools.cached_property
    def __segments(self) -> dict[int, list[_Message]]:
        segments: dict[int, list[_Message]] = {}
        for msg in self.__messages:
            segment = msg._filecfg.segment
            if segment in segments:
                segments[segment].append(msg)
            else:
                segments[segment] = [msg]
        return segments

    def __find_confluence(self, message: _Message) -> _Message | None:  # noqa: PLR0911
        """找到公共后继，主要为了找到选项终点合并后续重复项"""
        if message.confluence is not _uninit:
            return message.confluence  # pyright: ignore[reportReturnType]
        if message._filecfg.option_1 == "":  # 非选项短信，直接找 successor 字段，若无则找同段下一个
            if message._filecfg.successor != 0:
                confluence = self.__segments.get(message._filecfg.successor)
                message.confluence = confluence[0] if confluence is not None else None
                return message.confluence
            segments = self.__segments[message._filecfg.segment]
            index = next(index for index, msg in enumerate(segments) if msg.id == message.id)
            message.confluence = segments[index + 1] if index < len(segments) - 1 else None
            return message.confluence
        if message.option_index != 0:  # 含选项选择，且已经走到了选项对话处，找 successor 字段
            successors = (message._filecfg.option_successor_1, message._filecfg.option_successor_2)
            successor = successors[message.option_index - 1]
            if successor == 0:
                return None
            successor_segment = self.__segments.get(successor)
            message.confluence = successor_segment[0] if successor_segment is not None else None
            return message.confluence
        if message._filecfg.option_2 == "":  # 单选项选择，直接将选项对话作为下一个
            assert message.neighbours is not None
            message.confluence = message.neighbours[0]
            return message.confluence
        # 多选项字段，开始广搜找汇聚点
        queue: list[_Message | None] = list(message.successors)
        visit: dict[_Message, int] = collections.defaultdict(int)
        while any(msg is not None for msg in queue):
            for index, queue_msg in enumerate(queue):
                if queue_msg is None:
                    continue
                visit[queue_msg] += 1
                # self.__debug_visit(message, queue, visit)
                if visit[queue_msg] == len(queue):
                    message.confluence = queue_msg
                    return message.confluence
                queue[index] = self.__find_confluence(queue_msg)
        message.confluence = None
        return message.confluence

    def __wiki_write_message_single(self, wiki: typing.IO[str], indent: str, message: _Message):
        _ = wiki.write(indent)
        _ = wiki.write("{{短信对话|")
        _ = wiki.write("左" if message.option_index == 0 else "右")
        _ = wiki.write("|")
        if message.option_index == 0:
            _ = wiki.write(message.sender_name or message.sender_icon or "<未知>")
        else:
            _ = wiki.write("主角")
        if message.voice is not None:
            assert message.text is not None
            _ = wiki.write("|语音|")
            _ = wiki.write(message.text)
        elif message.image is not None:
            _ = wiki.write("|图片| <!-- ")
            _ = wiki.write(message.image)
            _ = wiki.write("-->")
        elif message.text is not None:
            _ = wiki.write("|文本|")
            _ = wiki.write(message.text)
        else:
            _ = wiki.write("}}")
            return
        _ = wiki.write("}}")

    def __wiki_write_message_select(
        self, wiki: typing.IO[str], indent: str, item: _Message, confluence: _Message | None
    ):
        assert item.option_1 is not None
        if item.option_2 is None:
            _ = wiki.write(indent)
            _ = wiki.write("{{短信对话|右|主角|选项|选项=")
            _ = wiki.write(item.option_1)
            _ = wiki.write("}}")
            return
        next_indent = indent + "  "
        _ = wiki.write(indent)
        _ = wiki.write("{{短信对话|右|主角|")
        if item._filecfg.type is message.Type.Option:
            _ = wiki.write("选项")
        elif item._filecfg.type is message.Type.ImageOption:
            _ = wiki.write("表情选项")
        _ = wiki.write(indent)
        _ = wiki.write("|选项1=")
        _ = wiki.write(item.option_1 if item._filecfg.type is message.Type.Option else item._filecfg.option_1)
        if item.successors[0] != confluence:
            _ = wiki.write(indent)
            _ = wiki.write("|剧情1=")
            self.__wiki_iter_message(wiki, next_indent, item.successors[0], confluence)
        _ = wiki.write(indent)
        _ = wiki.write("|选项2=")
        _ = wiki.write(item.option_2 if item._filecfg.type is message.Type.Option else item._filecfg.option_2)
        if item.successors[1] != confluence:
            _ = wiki.write(indent)
            _ = wiki.write("|剧情2=")
            self.__wiki_iter_message(wiki, next_indent, item.successors[1], confluence)
        _ = wiki.write(indent)
        _ = wiki.write("}}")

    def __wiki_iter_message(self, wiki: typing.IO[str], indent: str, message: _Message, confluence: _Message | None):
        if message == confluence:
            return
        next_confluence = self.__find_confluence(message)
        if not message.is_option_root:
            self.__wiki_write_message_single(wiki, indent, message)
        else:
            self.__wiki_write_message_select(wiki, indent, message, next_confluence)
        if next_confluence is not None:
            self.__wiki_iter_message(wiki, indent, next_confluence, confluence)

    def wiki(self) -> str:
        if 1 not in self.__segments or len(self.__segments[1]) == 0:
            return ""
        wiki = io.StringIO()
        message = self.__segments[1][0]
        self.__wiki_iter_message(wiki, "\n  ", message, None)
        return wiki.getvalue()


class MessageNPC(View[filecfg.MessageNPC]):
    FileCfg: typing.Final = filecfg.MessageNPC

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._filecfg.name)

    @property
    def icon(self) -> str:
        return self._filecfg.icon
