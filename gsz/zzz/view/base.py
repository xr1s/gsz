import typing

from ..filecfg import ModelID

if typing.TYPE_CHECKING:
    from ..data import GameData

E_co = typing.TypeVar("E_co", bound=ModelID, covariant=True)


class IView(typing.Protocol[E_co]):  # pyright: ignore[reportInvalidTypeVarUse]
    FileCfg: typing.ClassVar
    FileCfg: type[E_co]

    def __init__(self, game: "GameData", filecfg: E_co): ...


class View(typing.Generic[E_co]):
    def __init__(self, game: "GameData", filecfg: E_co):
        self._game: GameData = game
        self._filecfg: E_co = filecfg
