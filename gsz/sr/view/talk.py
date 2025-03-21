from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View


class TalkSentenceConfig(View[excel.TalkSentenceConfig]):
    ExcelOutput: typing.Final = excel.TalkSentenceConfig

    @functools.cached_property
    def text(self) -> str:
        return "" if self._excel.talk_sentence_text is None else self._game.text(self._excel.talk_sentence_text)

    @functools.cached_property
    def name(self) -> str:
        return (
            ""
            if self._excel.textmap_talk_sentence_name is None
            else self._game._plain_formatter.format(self._game.text(self._excel.textmap_talk_sentence_name))  # pyright: ignore[reportPrivateUsage]
        )

    @functools.cached_property
    def __voice(self) -> VoiceConfig | None:
        return None if self._excel.voice_id is None else self._game.voice_config(self._excel.voice_id)

    def voice(self) -> VoiceConfig | None:
        return None if self.__voice is None else VoiceConfig(self._game, self.__voice._excel)


class VoiceConfig(View[excel.VoiceConfig]):
    ExcelOutput: typing.Final = excel.VoiceConfig
