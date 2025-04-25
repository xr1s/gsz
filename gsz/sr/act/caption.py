from __future__ import annotations

import functools
import typing

if typing.TYPE_CHECKING:
    from ..data import GameData
    from . import model


class CaptionSentence:
    def __init__(self, game: GameData, caption: model.caption.CaptionSentence):
        self._game: GameData = game
        self._caption: model.caption.CaptionSentence = caption

    @functools.cached_property
    def text(self) -> str:
        return self._game.text(self._caption.caption_text_id)
