import typing

if typing.TYPE_CHECKING:
    from ..data import GameData
    from ..excel import ModelID, ModelMainSubID


class IView[E: ModelID | ModelMainSubID](typing.Protocol):
    ExcelOutput: typing.TypeAliasType

    def __init__(self, game: "GameData", excel: E): ...


class View[E: ModelID | ModelMainSubID]:
    def __init__(self, game: "GameData", excel: E):
        self._game: GameData = game
        self._excel: E = excel
