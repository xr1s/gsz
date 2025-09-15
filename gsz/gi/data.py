from __future__ import annotations

import collections
import collections.abc
import enum
import functools
import itertools
import json
import pathlib
import typing

import jinja2
import pydantic
import xxhash

from ..format import Formatter, Syntax
from . import view

if typing.TYPE_CHECKING:
    from . import excel
    from .excel import Text


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


V = typing.TypeVar("V", bound="view.IView[excel.ModelID]")


class excel_bin_output(typing.Generic[V]):
    """
    装饰器，接受参数为 View 类型
    View 类型中需要通过 ExcelBinOutput 类变量绑定映射数据结构类型

    装饰器会通过传入方法名找到数据目录中对应的文件名
    如果没找到，使用 *file_names 参数列表
    自动处理文件中的数据结构并且缓存，之后调用方法会返回完整列表、或通过 ID 返回对应结构

    具体的结构是一个巨大的 JSON Array
    Array 中的每一项都是一个 Object，包含需要的数据
    每个 Object 都会有一个唯一的 ID 字段（字段名未必就是 ID）
    """

    def __init__(self, typ: type[V], *file_names: str):
        self.__type = typ
        self.__file_names: tuple[str, ...] = file_names
        self.__excel_output: dict[int, excel.ModelID] | None = None

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
            if self.__excel_output is None:
                path = game.base / "ExcelBinOutput"
                file_names = iter(self.__file_names)
                file_path = path / (next(file_names) + "ExcelConfigData.json")
                try:
                    while not file_path.exists():
                        file_path = path / (next(file_names) + ".json")
                except StopIteration:
                    self.__excel_output = {}
                    return iter(()) if id is None or isinstance(id, collections.abc.Iterable) else None
                finally:
                    del self.__file_names  # 清理一下方便 GC
                ExcelBinOutputList = pydantic.TypeAdapter(list[self.__type.ExcelBinOutput | None])
                excels = json.loads(file_path.read_bytes())
                try:
                    excel_list = ExcelBinOutputList.validate_python(excels)
                    self.__excel_output = {config.id: config for config in excel_list if config is not None}
                except pydantic.ValidationError as exc:
                    ExcelBinOutputDict = pydantic.TypeAdapter(dict[int, self.__type.ExcelBinOutput])
                    try:
                        self.__excel_output = ExcelBinOutputDict.validate_python(excels)
                    except pydantic.ValidationError as former_structure_exc:
                        raise former_structure_exc from exc
            if id is None:
                return (self.__type(game, excel) for excel in self.__excel_output.values())
            if isinstance(id, collections.abc.Iterable):
                return (self.__type(game, self.__excel_output[k]) for k in id)
            excel = self.__excel_output.get(id)
            return None if excel is None else self.__type(game, excel)

        return fn


class GameDataStringMethod(typing.Protocol[T_co]):
    @typing.overload
    def __call__(self) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, id: str) -> T_co | None: ...


class GameDataStringFunction(typing.Protocol[T_co]):
    __name__: str

    @typing.overload
    def __get__(self, instance: GameData, owner: type[GameData]) -> GameDataStringMethod[T_co]: ...
    @typing.overload
    def __get__(self, instance: None, owner: type[GameData]) -> GameDataStringFunction[T_co]: ...
    @typing.overload
    def __call__(self, game: GameData) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, game: GameData, id: str) -> T_co | None: ...


VS = typing.TypeVar("VS", bound="view.IView[excel.ModelStringID]")


class excel_output_string(typing.Generic[VS]):
    """
    装饰器，接受参数为 View 类型
    View 类型中需要通过 ExcelBinOutput 类变量绑定映射数据结构类型

    装饰器会通过传入方法名找到数据目录中对应的文件名
    如果没找到，使用 *file_names 参数列表
    自动处理文件中的数据结构并且缓存，之后调用方法会返回完整列表、或通过 ID 返回对应结构

    具体的结构是一个巨大的 JSON Array
    Array 中的每一项都是一个 Object，包含需要的数据
    每个 Object 都会有一个唯一的 ID 字段（字段名未必就是 ID）

    举例来说
    ```json
    [
        {"ID": 1001, "Attr": ""},
        {"ID": 1002, "Attr": ""},
        {"ID": 1010, "Attr": ""},
        {"ID": 1011, "Attr": ""}
    ]
    ```

    2.3 及之前，结构是
    ```json
    {
        "1001": {"ID": 1001, "Attr": ""},
        "1002": {"ID": 1002, "Attr": ""},
        "1010": {"ID": 1010, "Attr": ""},
        "1011": {"ID": 1011, "Attr": ""}
    }
    ```
    """

    def __init__(self, typ: type[VS], *file_names: str):
        self.__type = typ
        self.__file_names: tuple[str, ...] = file_names
        self.__excel_output: dict[str, excel.ModelStringID] | None = None

    def __call__(self, method: typing.Callable[..., None]) -> GameDataStringFunction[VS]:
        if len(self.__file_names) == 0:
            self.__file_names = (file_name_generator(method.__name__),)

        @typing.overload
        def fn(game: GameData) -> collections.abc.Iterable[VS]: ...
        @typing.overload
        def fn(game: GameData, id: str) -> VS | None: ...
        def fn(game: GameData, id: str | None = None) -> VS | collections.abc.Iterable[VS] | None:
            if self.__excel_output is None:
                path = game.base / "ExcelBinOutput"
                file_names = iter(self.__file_names)
                file_path = path / (next(file_names) + ".json")
                try:
                    while not file_path.exists():
                        file_path = path / (next(file_names) + ".json")
                except StopIteration:
                    self.__excel_output = {}
                    return None
                finally:
                    del self.__file_names  # 清理一下方便 GC
                ExcelBinOutputList = pydantic.TypeAdapter(list[self.__type.ExcelBinOutput])
                excels = json.loads(file_path.read_bytes())
                self.__excel_output = {config.id: config for config in ExcelBinOutputList.validate_python(excels)}
            if id is None:
                return (self.__type(game, excel) for excel in self.__excel_output.values())
            excel = self.__excel_output.get(id)
            return None if excel is None else self.__type(game, excel)

        return fn


class GameDataMainSubMethod(typing.Protocol[T_co]):
    @typing.overload
    def __call__(self) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, main_id: int) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, main_id: int, sub_id: int) -> T_co | None: ...


class GameDataMainSubFunction(typing.Protocol[T_co]):
    __name__: str

    @typing.overload
    def __get__(self, instance: GameData, owner: type[GameData]) -> GameDataMainSubMethod[T_co]: ...
    @typing.overload
    def __get__(self, instance: None, owner: type[GameData]) -> GameDataMainSubFunction[T_co]: ...
    @typing.overload
    def __call__(self, game: GameData) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, game: GameData, main_id: int) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, game: GameData, main_id: int, sub_id: int) -> T_co | None: ...


MSV = typing.TypeVar("MSV", bound="view.IView[excel.ModelMainSubID]")


class excel_output_main_sub(typing.Generic[MSV]):
    """
    装饰器，类似 excel_output，接受参数为 View 类型
    View 类型中需要通过 ExcelBinOutput 类变量绑定映射数据结构类型

    装饰器会通过传入方法名找到数据目录中对应的文件名
    如果没找到，使用 *file_names 参数列表
    自动处理文件中的数据结构并且缓存，之后调用方法会返回完整列表、或通过 ID 返回对应结构

    具体的结构是一个巨大的 JSON Array
    Array 中的每一项都是一个 Object，包含需要的数据

    和 excel_output 不同的是
    每个 Object 都会有一个主要的 ID 和次要的 SubID 字段（字段名未必就是这两个）
    二元组 (ID, SubID) 在文件中是唯一的，但是 ID 和 SubID 本身可能重复

    举例来说
    ```json
    [
        {"ID": 1001, "Lv": 1, "Attr": ""},
        {"ID": 1001, "Lv": 2, "Attr": ""},
        {"ID": 1010, "Lv": 10, "Attr": ""},
        {"ID": 1010, "Lv": 11, "Attr": ""}
    ]
    ```

    2.3 及之前，结构是
    ```json
    {
      "1001": {
        {"1": {"ID": 1001, "Lv": 1, "Attr": ""}},
        {"2": {"ID": 1001, "Lv": 2, "Attr": ""}}
      },
      "1010": {
        {"10": {"ID": 1010, "Lv": 10, "Attr": ""}},
        {"11": {"ID": 1010, "Lv": 11, "Attr": ""}}
      }
    }
    ```
    """

    def __init__(self, typ: type[MSV], *file_names: str):
        self.__type = typ
        self.__file_names: tuple[str, ...] = file_names
        self.__excel_output: dict[int, list[excel.ModelMainSubID]] | None = None

    def __call__(self, method: typing.Callable[..., None]) -> GameDataMainSubFunction[MSV]:
        if len(self.__file_names) == 0:
            self.__file_names = (file_name_generator(method.__name__),)

        @typing.overload
        def fn(game: GameData) -> collections.abc.Iterable[MSV]: ...
        @typing.overload
        def fn(game: GameData, main_id: int) -> collections.abc.Iterable[MSV]: ...
        @typing.overload
        def fn(game: GameData, main_id: int, sub_id: int) -> MSV | None: ...
        def fn(
            game: GameData, main_id: int | None = None, sub_id: int | None = None
        ) -> MSV | collections.abc.Iterable[MSV] | None:
            if self.__excel_output is None:
                path = game.base / "ExcelBinOutput"
                file_names = iter(self.__file_names)
                file_path = path / (next(file_names) + ".json")
                try:
                    while not file_path.exists():
                        file_path = path / (next(file_names) + ".json")
                except StopIteration:
                    self.__excel_output = {}
                    return iter(()) if main_id is None or sub_id is None else None
                finally:
                    del self.__file_names  # 清理一下方便 GC
                ExcelBinOutputList = pydantic.TypeAdapter(list[self.__type.ExcelBinOutput | None])
                excels = json.loads(file_path.read_bytes())
                try:
                    excel_list = ExcelBinOutputList.validate_python(excels)
                    self.__excel_output = collections.defaultdict(list)
                    for excel in filter(None, excel_list):
                        self.__excel_output[excel.main_id].append(excel)
                except pydantic.ValidationError as exc:
                    ExcelBinOutputDict = pydantic.TypeAdapter(dict[int, dict[int, self.__type.ExcelBinOutput]])
                    try:
                        excel_dict = ExcelBinOutputDict.validate_python(excels)
                    except pydantic.ValidationError as former_structure_exc:
                        raise former_structure_exc from exc
                    self.__excel_output = {main_id: list(excel.values()) for main_id, excel in excel_dict.items()}
            match main_id, sub_id:
                case None, None:
                    excels = self.__excel_output.values()
                    return (self.__type(game, excel) for excel in itertools.chain.from_iterable(excels))
                case main_id, None:
                    return (self.__type(game, excel) for excel in self.__excel_output.get(main_id, ()))
                case None, sub_id:
                    raise ValueError("main_id cannot be none when sub_id is not None")
                case main_id, sub_id:
                    gen = (
                        self.__type(game, excel)
                        for excel in self.__excel_output.get(main_id, ())
                        if excel.sub_id == sub_id
                    )
                    return next(gen, None)

        return fn


NE_co = typing.TypeVar("NE_co", bound="excel.ModelID | excel.ModelMainSubID", covariant=True)


class PropertyName(typing.Protocol[NE_co]):
    _excel: NE_co

    def __init__(self, game: GameData, excel: NE_co): ...

    @property
    def name(self) -> str: ...


class CachedPropertyName(typing.Protocol[NE_co]):
    _excel: NE_co

    def __init__(self, game: GameData, excel: NE_co): ...

    @functools.cached_property
    def name(self) -> str: ...


NV = typing.TypeVar(
    "NV",
    bound="PropertyName[excel.ModelID | excel.ModelMainSubID] | CachedPropertyName[excel.ModelID | excel.ModelMainSubID]",
)


class excel_output_name(typing.Generic[NV]):
    def __init__(self, typ: type[NV], method: GameDataFunction[NV] | GameDataMainSubFunction[NV]):
        self.__type = typ
        self.__method = method
        self.__excel_output: dict[str, list[excel.ModelID | excel.ModelMainSubID]] | None = None

    def __call__(self, _method: typing.Callable[..., None]) -> typing.Callable[[GameData, str], list[NV]]:
        def fn(game: GameData, name: str) -> list[NV]:
            if self.__excel_output is None:
                self.__excel_output = {}
                for view in self.__method(game):
                    excel = view._excel  # pyright: ignore[reportPrivateUsage]
                    if view.name in self.__excel_output:
                        self.__excel_output[view.name].append(excel)
                    else:
                        self.__excel_output[view.name] = [excel]
            excel_list = self.__excel_output.get(name)
            return [] if excel_list is None else [self.__type(game, excel) for excel in excel_list]

        return fn


class Language(enum.Enum):
    CHS = "CHS"
    """简体中文"""
    CHT = "CHT"
    """繁体中文"""
    DE = "DE"
    """德文"""
    EN = "EN"
    """英文"""
    ES = "ES"
    """西班牙文"""
    FR = "FR"
    """法文"""
    ID = "ID"
    """印尼文"""
    JP = "JP"
    """日文"""
    KR = "KR"
    """韩文"""
    PT = "PT"
    """葡萄牙文"""
    RU = "RU"
    """俄文"""
    TH = "TH"
    """泰文"""
    VI = "VI"
    """越文"""

    def candidates(self) -> list[str]:
        if self == self.CHS:
            return ["CN", "CHS"]
        return [self.value]


class GameData:
    def __init__(self, base: str | pathlib.Path, *, language: Language = Language.CHS):
        self.base: pathlib.Path = pathlib.Path(base)
        self.__default_language: Language = language
        self.__text_map: dict[Language, dict[int, str]] = {}

    def __load_text_map(self, language: Language) -> dict[int, str]:
        candidates = iter(language.candidates())
        text_map_path = self.base / "TextMap" / f"TextMap{next(candidates)}.json"
        while not text_map_path.exists():
            text_map_path: pathlib.Path = self.base / "TextMap" / f"TextMap{next(candidates)}.json"
        text_map = text_map_path.read_bytes()
        return pydantic.TypeAdapter(dict[int, str]).validate_json(text_map)

    def text(self, key: Text, *, language: Language | None = None) -> str:
        language = language or Language.CHS
        if language not in self.__text_map:
            text_map = self.__load_text_map(language)
            self.__text_map[language] = text_map
        else:
            text_map = self.__text_map[language]
        return text_map.get(key, "")

    @functools.cached_property
    def _plain_formatter(self) -> Formatter:
        return Formatter(game=self)

    @functools.cached_property
    def _mw_formatter(self) -> Formatter:
        return Formatter(syntax=Syntax.MediaWiki, game=self)

    @functools.cached_property
    def _mw_pretty_formatter(self) -> Formatter:
        return Formatter(syntax=Syntax.MediaWikiPretty, game=self)

    @functools.cached_property
    def _template_environment(self) -> jinja2.Environment:
        self_path = pathlib.Path(__file__)
        templates_path = self_path.parent / "templates"
        env = jinja2.Environment(
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="${",
            variable_end_string="}",
            comment_start_string="%",
            comment_end_string="\n",
            loader=jinja2.FileSystemLoader(templates_path),
        )
        env.filters.update(
            gszformat=self._mw_formatter.format,
            gszformat_pretty=self._mw_pretty_formatter.format,
            zip=zip,  # pyright: ignore[reportArgumentType]
        )
        return env

    ######## avatar ########

    @excel_bin_output(view.Avatar)
    def avatar(self):
        """角色"""

    @excel_bin_output(view.AvatarSkill)
    def avatar_skill(self):
        """角色技能"""

    @excel_bin_output(view.AvatarSkillDepot)
    def avatar_skill_depot(self):
        """角色技能组"""
