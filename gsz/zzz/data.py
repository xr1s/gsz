from __future__ import annotations

import collections.abc
import enum
import functools
import pathlib
import typing

import pydantic

from . import filecfg, view

T_co = typing.TypeVar("T_co", covariant=True)


class GameDataMethod(typing.Protocol[T_co]):
    @typing.overload
    def __call__(self) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, id: int) -> T_co | None: ...
    @typing.overload
    def __call__(self, id: collections.abc.Iterable[int]) -> collections.abc.Iterable[T_co]: ...


class GameDataFunction(typing.Protocol[T_co]):
    __name__: str

    @typing.overload
    def __get__(self, instance: GameData, owner: type[GameData]) -> GameDataMethod[T_co]: ...
    @typing.overload
    def __get__(self, instance: None, owner: type[GameData]) -> GameDataFunction[T_co]: ...
    @typing.overload
    def __call__(self, game: GameData) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, game: GameData, id: int) -> T_co | None: ...
    @typing.overload
    def __call__(self, game: GameData, id: collections.abc.Iterable[int]) -> collections.abc.Iterable[T_co]: ...


ABBR_WORDS = {"npc", "cg"}


def file_name_generator(method_name: str) -> str:
    return "".join(word.upper() if word in ABBR_WORDS else word.capitalize() for word in method_name.split("_"))


V = typing.TypeVar("V", bound="view.IView[filecfg.ModelID]")


class file_cfg(typing.Generic[V]):
    """
    装饰器，接受参数为 View 类型
    View 类型中需要通过 FileCfg 类变量绑定映射数据结构类型

    装饰器会通过传入方法名找到数据目录中对应的文件名
    如果没找到，使用 *file_names 参数列表
    自动处理文件中的数据结构并且缓存，之后调用方法会返回完整列表、或通过 ID 返回对应结构

    具体的结构是一个单字段的 Object，内有一个巨大的 JSON Array
    Array 中的每一项都是一个 Object，包含需要的数据
    每个 Object 都会有一个唯一的 ID 字段（字段名未必就是 ID）

    举例来说:
    ```json
    {
        "__exp_FileCfg": [
            {"ID": 1001, "Attr": ""},
            {"ID": 1002, "Attr": ""},
            {"ID": 1010, "Attr": ""},
            {"ID": 1011, "Attr": ""}
        ]
    }
    ```
    """

    def __init__(self, typ: type[V], *file_names: str):
        self.__type = typ
        self.__file_names: tuple[str, ...] = file_names
        self.__filecfg: dict[int, filecfg.ModelID] | None = None

    def __call__(self, method: typing.Callable[..., None]) -> GameDataFunction[V]:
        if len(self.__file_names) == 0:
            self.__file_names = (file_name_generator(method.__name__),)

        @typing.overload
        def fn(game: GameData) -> collections.abc.Iterable[V]: ...
        @typing.overload
        def fn(game: GameData, id: int) -> V | None: ...
        @typing.overload
        def fn(game: GameData, id: collections.abc.Iterable[int]) -> collections.abc.Iterable[V]: ...
        def fn(
            game: GameData, id: int | collections.abc.Iterable[int] | None = None
        ) -> V | collections.abc.Iterable[V] | None:
            if self.__filecfg is None:
                path = game.base / "FileCfg"
                file_names = iter(self.__file_names)
                file_path = path / (next(file_names) + "TemplateTb.json")
                try:
                    while not file_path.exists():
                        file_path = path / (next(file_names) + ".json")
                except StopIteration:
                    self.__filecfg = {}
                    return iter(()) if id is None or isinstance(id, collections.abc.Iterable) else None
                finally:
                    del self.__file_names  # 清理一下方便 GC
                filecfgs = filecfg.ExpFileCfg[self.__type.FileCfg].model_validate_json(file_path.read_bytes())
                self.__filecfg = {filecfg.id: filecfg for filecfg in filecfgs.exp_filecfg}
            if id is None:
                return (self.__type(game, cfg) for cfg in self.__filecfg.values())
            if isinstance(id, collections.abc.Iterable):
                return (self.__type(game, self.__filecfg[k]) for k in id)
            cfg = self.__filecfg.get(id)
            return None if cfg is None else self.__type(game, cfg)

        return fn


class Language(enum.Enum):
    CHT = "_CHT"
    DE = "_DE"
    EN = "_EN"
    ES = "_ES"
    FR = "_FR"
    ID = "_ID"
    JA = "_JA"
    KO = "_KO"
    PT = "_PT"
    RU = "_RU"
    TH = "_TH"
    VI = "_VI"


class GameData:
    def __init__(self, base: str | pathlib.Path, *, language: Language | None = None):
        self.base: pathlib.Path = pathlib.Path(base)
        lang = language.value if language is not None else ""
        text_map_path = self.base / "TextMap" / f"TextMap{lang}TemplateTb.json"
        text_map = text_map_path.read_bytes()
        self.__text_map = pydantic.TypeAdapter(dict[str, str]).validate_json(text_map)

    def text(self, text: str) -> str:
        return self.__text_map.get(text, "")

    ######## message ########

    @file_cfg(view.DirectoryConfig)
    def directory_config(self):
        """knock knock 联系人介绍"""

    @file_cfg(view.MessageConfig)
    def message_config(self):
        """knock knock 聊天内容"""

    @file_cfg(view.MessageGroupConfig)
    def message_group_config(self):
        """一次 knock knock 聊天"""

    @functools.cached_property
    def _messages_of_group(self) -> dict[int, list[filecfg.MessageConfig]]:
        groups: dict[int, list[filecfg.MessageConfig]] = {}
        for message in self.message_config():
            cfg = message._filecfg  # pyright: ignore[reportPrivateUsage]
            if cfg.group_id in groups:
                groups[cfg.group_id].append(cfg)
            else:
                groups[cfg.group_id] = [cfg]
        return groups

    @file_cfg(view.MessageNPC)
    def message_npc(self):
        """knock knock 中的非自机角色联系人"""

    ######## partner ########
    @file_cfg(view.PartnerConfig)
    def partner_config(self):
        """可能包含 NPC 的联系人"""
