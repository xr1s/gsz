from __future__ import annotations
import pathlib
import typing

from .. import story


if typing.TYPE_CHECKING:
    from ..data import GameData


class Story:
    def __init__(self, game: GameData, excel: pathlib.Path | story.Story):
        self._game: GameData = game
        self._story: story.Story = (
            excel
            if isinstance(excel, story.Story)
            else story.Story.model_validate_json(game.base.joinpath(excel).read_bytes())
        )

    # 模拟宇宙对话，先简单处理
    def rogue_talk(self):
        pass
