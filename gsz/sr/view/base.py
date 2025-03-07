import typing

if typing.TYPE_CHECKING:
    from ..data import GameData


class View[E]:
    def __init__(self, game: "GameData", excel: E):
        self._game: GameData = game
        self._excel: E = excel
