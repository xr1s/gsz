import collections
import collections.abc
import enum
import functools
import itertools
import pathlib
import typing

import jinja2
import pydantic

from . import view
from ..format import Formatter, Syntax

if typing.TYPE_CHECKING:
    from .excel import Text


class GameDataMethod[T](typing.Protocol):
    @typing.overload
    def __call__(self) -> collections.abc.Iterable[T]: ...
    @typing.overload
    def __call__(self, id: int) -> T | None: ...
    @typing.overload
    def __call__(self, id: collections.abc.Iterable[int]) -> collections.abc.Iterable[T]: ...


class GameDataFunction[T](typing.Protocol):
    __name__: str

    @typing.overload
    def __get__(self, instance: "GameData", owner: type["GameData"]) -> GameDataMethod[T]: ...
    @typing.overload
    def __get__(self, instance: None, owner: type["GameData"]) -> "GameDataFunction[T]": ...
    @typing.overload
    def __call__(self, game: "GameData") -> collections.abc.Iterable[T]: ...
    @typing.overload
    def __call__(self, game: "GameData", id: int) -> T | None: ...
    @typing.overload
    def __call__(self, game: "GameData", id: collections.abc.Iterable[int]) -> collections.abc.Iterable[T]: ...


class ID(typing.Protocol):
    def id(self) -> int: ...


E_co = typing.TypeVar("E_co", bound=ID, covariant=True)


class View(typing.Generic[E_co], typing.Protocol):
    ExcelOutput: typing.TypeAliasType

    def __init__(self, game: "GameData", excel: E_co): ...


V = typing.TypeVar("V", bound=View[ID])


ABBR_WORDS = {"npc"}


def file_name_generator(method_name: str) -> str:
    return "".join(word.upper() if word in ABBR_WORDS else word.capitalize() for word in method_name.split("_"))


class excel_output(typing.Generic[V, E_co]):
    """
    装饰器，接受参数为 View 类型
    View 类型中需要通过 ExcelOutput 类变量绑定映射数据结构类型

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

    def __init__(self, typ: type[V], *file_names: str):
        self.__type = typ
        self.__file_names: tuple[str, ...] = file_names
        self.__excel_output: dict[int, E_co] | None = None

    def __call__(self, method: typing.Callable[..., None]) -> GameDataFunction[V]:
        if len(self.__file_names) == 0:
            self.__file_names = (file_name_generator(method.__name__),)

        @typing.overload
        def fn(game: "GameData") -> collections.abc.Iterable[V]: ...
        @typing.overload
        def fn(game: "GameData", id: int) -> V | None: ...
        @typing.overload
        def fn(game: "GameData", id: collections.abc.Iterable[int]) -> collections.abc.Iterable[V]: ...
        def fn(
            game: "GameData", id: int | collections.abc.Iterable[int] | None = None
        ) -> V | collections.abc.Iterable[V] | None:
            if self.__excel_output is None:
                path = game.base / "ExcelOutput"
                file_names = iter(self.__file_names)
                file_path = path / (next(file_names) + ".json")
                try:
                    while not file_path.exists():
                        file_path = path / (next(file_names) + ".json")
                except StopIteration:
                    self.__excel_output = {}
                    if id is None or isinstance(id, collections.abc.Iterable):
                        return iter(())
                    return None
                finally:
                    self.__file_names = ()  # 清理一下方便 GC
                ExcelOutput = typing.cast(E_co, typing.cast(typing.Any, self.__type.ExcelOutput))
                # TODO: 支持 2.3 之前数据格式载入
                ExcelOutputList = pydantic.TypeAdapter(list[ExcelOutput])
                json = ExcelOutputList.validate_json(file_path.read_bytes())
                self.__excel_output = {config.id(): config for config in json}
            if id is None:
                return (self.__type(game, excel) for excel in self.__excel_output.values())
            if isinstance(id, collections.abc.Iterable):
                return (self.__type(game, self.__excel_output[k]) for k in id)
            excel = self.__excel_output.get(id)
            return None if excel is None else self.__type(game, excel)

        return fn


class GameDataMainSubMethod[T](typing.Protocol):
    @typing.overload
    def __call__(self) -> collections.abc.Iterable[T]: ...
    @typing.overload
    def __call__(self, main_id: int) -> collections.abc.Iterable[T]: ...
    @typing.overload
    def __call__(self, main_id: int, sub_id: int) -> T | None: ...


class GameDataMainSubFunction[T](typing.Protocol):
    __name__: str

    @typing.overload
    def __get__(self, instance: "GameData", owner: type["GameData"]) -> GameDataMainSubMethod[T]: ...
    @typing.overload
    def __get__(self, instance: None, owner: type["GameData"]) -> "GameDataMainSubFunction[T]": ...
    @typing.overload
    def __call__(self, game: "GameData") -> collections.abc.Iterable[T]: ...
    @typing.overload
    def __call__(self, game: "GameData", main_id: int) -> collections.abc.Iterable[T]: ...
    @typing.overload
    def __call__(self, game: "GameData", main_id: int, sub_id: int) -> T | None: ...


class MainSubID(typing.Protocol):
    def main_id(self) -> int: ...
    def sub_id(self) -> int: ...


MSE_co = typing.TypeVar("MSE_co", bound=MainSubID, covariant=True)


class MainSubView(typing.Generic[MSE_co], typing.Protocol):
    ExcelOutput: typing.TypeAliasType

    def __init__(self, game: "GameData", excel: MSE_co): ...


MSV = typing.TypeVar("MSV", bound=MainSubView[MainSubID])


class excel_output_main_sub(typing.Generic[MSV, MSE_co]):
    """
    装饰器，类似 excel_output，接受参数为 View 类型
    View 类型中需要通过 ExcelOutput 类变量绑定映射数据结构类型

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
        self.__excel_output: dict[int, list[MSE_co]] | None = None

    def __call__(self, method: typing.Callable[..., None]) -> GameDataMainSubFunction[MSV]:
        if len(self.__file_names) == 0:
            self.__file_names = (file_name_generator(method.__name__),)

        @typing.overload
        def fn(game: "GameData") -> collections.abc.Iterable[MSV]: ...
        @typing.overload
        def fn(game: "GameData", main_id: int) -> collections.abc.Iterable[MSV]: ...
        @typing.overload
        def fn(game: "GameData", main_id: int, sub_id: int) -> MSV | None: ...
        def fn(
            game: "GameData", main_id: int | None = None, sub_id: int | None = None
        ) -> MSV | collections.abc.Iterable[MSV] | None:
            if self.__excel_output is None:
                path = game.base / "ExcelOutput"
                file_names = iter(self.__file_names)
                file_path = path / (next(file_names) + ".json")
                try:
                    while not file_path.exists():
                        file_path = path / (next(file_names) + ".json")
                except StopIteration:
                    self.__excel_output = {}
                    if main_id is None or sub_id is None:
                        return iter(())
                    return None
                finally:
                    self.__file_names = ()  # 清理一下方便 GC
                ExcelOutput = typing.cast(MSE_co, typing.cast(typing.Any, self.__type.ExcelOutput))
                # TODO: 支持 2.3 之前数据格式载入
                ExcelOutputList = pydantic.TypeAdapter(list[ExcelOutput])
                json = ExcelOutputList.validate_json(file_path.read_bytes())
                self.__excel_output = {}
                for excel in json:
                    id = excel.main_id()
                    if self.__excel_output.get(id, None) is None:
                        self.__excel_output[id] = [excel]
                    else:
                        self.__excel_output[id].append(excel)
            match main_id, sub_id:
                case None, None:
                    excels = self.__excel_output.values()
                    return (self.__type(game, excel) for excel in itertools.chain.from_iterable(excels))
                case main_id, None:
                    return (self.__type(game, excel) for excel in self.__excel_output.get(main_id, []))
                case None, sub_id:
                    raise ValueError("main_id cannot be none when sub_id is not None")
                case main_id, sub_id:
                    return next(
                        (
                            self.__type(game, excel)
                            for excel in self.__excel_output.get(main_id, [])
                            if excel.sub_id() == sub_id
                        ),
                        None,
                    )

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
        candidates = iter(language.candidates())
        text_map_path = self.base / "TextMap" / f"TextMap{next(candidates)}.json"
        while not text_map_path.exists():
            text_map_path: pathlib.Path = self.base / "TextMap" / f"TextMap{next(candidates)}.json"
        text_map = text_map_path.read_bytes()
        self.__text_map = pydantic.TypeAdapter(dict[int, str]).validate_json(text_map)

    def text(self, text: "Text") -> str:
        return self.__text_map.get(text.hash, "")

    @functools.cached_property
    def template_environment(self):
        formatter = Formatter(syntax=Syntax.MediaWiki, game=self)
        env = jinja2.Environment(
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="${",
            variable_end_string="}",
            comment_start_string="%",
            loader=jinja2.FileSystemLoader("./templates"),
        )
        env.filters.update(gszformat=formatter.format)
        return env

    ######## misc ########
    @excel_output(view.ExtraEffectConfig)
    def extra_effect_config(self):
        """效果说明"""

    @functools.cached_property
    def extra_effect_config_names(self) -> set[str]:
        return {effect.name for effect in self.extra_effect_config()}

    ######## monster ########

    @excel_output(view.EliteGroup)
    def elite_group(self):
        """精英组别"""

    @excel_output_main_sub(view.HardLevelGroup)
    def hard_level_group(self):
        """敌人属性成长详情"""

    @excel_output(view.MonsterCamp)
    def monster_camp(self):
        """敌人阵营"""

    @excel_output(view.MonsterConfig)
    def monster_config(self):
        """敌人详情"""

    @excel_output(view.MonsterSkillConfig)
    def monster_skill_config(self):
        """敌人技能"""

    @excel_output(view.MonsterTemplateConfig)
    def monster_template_config(self):
        """敌人模板详情"""

    @excel_output(view.MonsterTemplateConfig)
    def monster_template_unique_config(self):
        """敌人模板（不清楚和不带 unique 的什么区别，不过有时候两个都要查）"""

    @functools.cached_property
    def monster_template_group(self):
        template_groups: dict[int, list[int]] = {}
        for template in self.monster_template_config():
            group_id = template.group_id
            if group_id is None:
                continue
            if template_groups.get(group_id) is None:
                template_groups[group_id] = [group_id]
            else:
                template_groups[group_id].append(group_id)
        return template_groups

    @excel_output(view.NPCMonsterData)
    def npc_monster_data(self):
        """敌人详情"""
