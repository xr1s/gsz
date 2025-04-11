import typing

from ..excel import ModelID, ModelMainSubID, ModelStringID

if typing.TYPE_CHECKING:
    from ..data import GameData

E_co = typing.TypeVar("E_co", bound=ModelID | ModelStringID | ModelMainSubID, covariant=True)


class IView(typing.Protocol[E_co]):  # pyright: ignore[reportInvalidTypeVarUse]
    ExcelOutput: typing.ClassVar
    ExcelOutput: type[E_co]

    def __init__(self, game: "GameData", excel: E_co): ...


class View(typing.Generic[E_co]):
    def __init__(self, game: "GameData", excel: E_co):
        self._game: GameData = game
        self._excel: E_co = excel
