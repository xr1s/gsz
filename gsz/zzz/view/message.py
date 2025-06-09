from __future__ import annotations

import functools
import typing

from .. import filecfg
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

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

    @functools.cached_property
    def text(self):
        """文本消息，保证有文本时无选项，有选项时无文本"""
        return self._game.text(self._filecfg.text)

    @functools.cached_property
    def options(self) -> tuple[str, str] | None:
        """选项消息，保证有文本时无选项，有选项时无文本"""
        if self._filecfg.option_1 == "" and self._filecfg.option_2 == "":
            return None
        option_01 = self._game.text(self._filecfg.option_1)
        option_02 = self._game.text(self._filecfg.option_2)
        if option_01 == "" and option_02 == "":
            return None
        return option_01, option_02

    @functools.cached_property
    def options_long(self) -> tuple[str, str] | None:
        """选择对应选项后实际回复的消息正文，可能和选项本身文本相同"""
        if self._filecfg.option_long_1 == "" and self._filecfg.option_long_2 == "":
            return None
        option_01 = self._game.text(self._filecfg.option_long_1)
        option_02 = self._game.text(self._filecfg.option_long_2)
        if option_01 == "" and option_02 == "":
            return None
        return option_01, option_02

    @functools.cached_property
    def __group(self) -> MessageGroupConfig | None:
        return self._game.message_group_config(self._filecfg.group_id)

    def group(self) -> MessageGroupConfig | None:
        return None if self.__group is None else MessageGroupConfig(self._game, self.__group._filecfg)

    @functools.cached_property
    def __directory(self) -> DirectoryConfig | None:
        return self._game.directory_config(self._filecfg.sender_id)

    @functools.cached_property
    def __npc(self) -> MessageNPC | None:
        return self._game.message_npc(self._filecfg.sender_id)

    @functools.cached_property
    def sender_name(self) -> str:
        if self._filecfg.sender_id == 0:
            return "绳匠"
        sender = self.__directory.partner() if self.__directory is not None else self.__npc
        return sender.name if sender is not None else ""

    @functools.cached_property
    def sender_icon(self) -> str | None:
        if self._filecfg.sender_id == 0:
            return None
        return self.__npc.icon if self.__npc is not None else None


class MessageGroupConfig(View[filecfg.MessageGroupConfig]):
    FileCfg: typing.Final = filecfg.MessageGroupConfig

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
    def __messages(self) -> list[filecfg.MessageConfig]:
        return self._game._messages_of_group.get(self._filecfg.id, [])  # pyright: ignore[reportPrivateUsage]

    def messages(self) -> collections.abc.Iterable[MessageConfig]:
        return (MessageConfig(self._game, message) for message in self.__messages)

    @functools.cached_property
    def __quests(self) -> list[QuestConfig]:
        return list(
            self._game.quest_config(
                quest_id for quest_id in self._filecfg.quest_ids if quest_id not in {12080101, 12080102, 1300301210}
            )
        )

    def quests(self) -> collections.abc.Iterable[QuestConfig]:
        from .quest import QuestConfig

        return (QuestConfig(self._game, quest._filecfg) for quest in self.__quests)


class MessageNPC(View[filecfg.MessageNPC]):
    FileCfg: typing.Final = filecfg.MessageNPC

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._filecfg.name)

    @property
    def icon(self) -> str:
        return self._filecfg.icon
