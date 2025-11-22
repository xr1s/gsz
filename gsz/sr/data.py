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


class excel_output(typing.Generic[V]):
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
                path = game.base / "ExcelOutput"
                file_names = iter(self.__file_names)
                file_path = path / (next(file_names) + ".json")
                try:
                    while not file_path.exists():
                        file_path = path / (next(file_names) + ".json")
                except StopIteration:
                    self.__excel_output = {}
                    return iter(()) if id is None or isinstance(id, collections.abc.Iterable) else None
                finally:
                    del self.__file_names  # 清理一下方便 GC
                # ItemConfigAvatarSkin.json 由于内容仍未上线而数据文件已经存在（尽管之前一直为空）
                # 可能是清理测试数据缺漏导致出现大量 null（此前 2.3 之前无，可能和修改数据格式有关），额外过滤一下
                ExcelOutputList = pydantic.TypeAdapter(list[self.__type.ExcelOutput | None])
                excels = json.loads(file_path.read_bytes())
                try:
                    excel_list = ExcelOutputList.validate_python(excels)
                    self.__excel_output = {config.id: config for config in excel_list if config is not None}
                except pydantic.ValidationError as exc:
                    ExcelOutputDict = pydantic.TypeAdapter(dict[int, self.__type.ExcelOutput])
                    try:
                        self.__excel_output = ExcelOutputDict.validate_python(excels)
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
                path = game.base / "ExcelOutput"
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
                ExcelOutputList = pydantic.TypeAdapter(list[self.__type.ExcelOutput])
                excels = json.loads(file_path.read_bytes())
                self.__excel_output = {config.id: config for config in ExcelOutputList.validate_python(excels)}
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
                path = game.base / "ExcelOutput"
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
                ExcelOutputList = pydantic.TypeAdapter(list[self.__type.ExcelOutput | None])
                excels = json.loads(file_path.read_bytes())
                try:
                    excel_list = ExcelOutputList.validate_python(excels)
                    self.__excel_output = collections.defaultdict(list)
                    for excel in filter(None, excel_list):
                        self.__excel_output[excel.main_id].append(excel)
                except pydantic.ValidationError as exc:
                    ExcelOutputDict = pydantic.TypeAdapter(dict[int, dict[int, self.__type.ExcelOutput]])
                    try:
                        excel_dict = ExcelOutputDict.validate_python(excels)
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

    @staticmethod
    def __int32(integer: int) -> int:
        return (integer & 0xFFFFFFFF ^ 0x80000000) - 0x80000000

    @staticmethod
    def __stable_hash(key: str) -> int:
        hashes = [5381, 5381]
        for index, char in enumerate(key):
            hashes[index & 1] = GameData.__int32(hashes[index & 1] << 5) + hashes[index & 1] ^ ord(char)
        return GameData.__int32(hashes[0] + hashes[1] * 1566083941)

    def text(self, key: Text, *, language: Language | None = None) -> str:
        language = language or self.__default_language
        if language not in self.__text_map:
            text_map = self.__load_text_map(language)
            self.__text_map[language] = text_map
        else:
            text_map = self.__text_map[language]
        if isinstance(key, str):
            # 老版本使用 xxh32，后面改成 xxh64 了，为了兼容两个都试一下
            xxh64 = xxhash.xxh64_intdigest(key)
            return text_map.get(xxh64) or text_map.get(self.__stable_hash(key), "")
        return text_map.get(key.hash, "")

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

    @excel_output(view.AtlasAvatarChangeInfo)
    def atlas_avatar_change_info(self):
        """角色阵营变更，如完成对应任务后，黄泉从巡海游侠变为自灭者，星期日从匹诺康尼变为银河"""

    @functools.cached_property
    def _atlas_change_info_avatar_config(self) -> dict[int, excel.AtlasAvatarChangeInfo]:
        return {change._excel.avatar_id: change._excel for change in self.atlas_avatar_change_info()}  # pyright: ignore[reportPrivateUsage]

    @excel_output(view.AvatarAtlas)
    def avatar_atlas(self):
        """角色阵营、配音演员"""

    @excel_output(view.AvatarCamp)
    def avatar_camp(self):
        """角色阵营"""

    @excel_output(view.AvatarConfig)
    def avatar_config(self):
        """角色"""

    @excel_output(view.AvatarConfig, "AvatarConfigLD")
    def avatar_config_ld(self):
        """Fate 联动自机角色"""

    @excel_output(view.AvatarPlayerIcon)
    def avatar_player_icon(self):
        """角色对应的玩家头像"""

    @excel_output_main_sub(view.AvatarPromotionConfig)
    def avatar_promotion_config(self):
        """角色突破需要素材、提升属性"""

    @excel_output(view.AvatarRankConfig)
    def avatar_rank_config(self):
        """角色命座"""

    @excel_output_main_sub(view.AvatarSkillConfig)
    def avatar_servant_skill_config(self):
        """忆灵技能"""

    @excel_output_main_sub(view.AvatarSkillConfig)
    def avatar_skill_config(self):
        """
        角色的所有技能
        举例来说：丹恒饮月的普攻和强化普攻这里分两种，AvatarSkillTreeConfig 都算在普攻中
        """

    @excel_output_main_sub(view.AvatarSkillConfig, "AvatarSkillConfigLD")
    def avatar_skill_config_ld(self):
        """联动角色的所有技能"""

    @excel_output_main_sub(view.AvatarSkillTreeConfig)
    def avatar_skill_tree_config(self):
        """角色详情页的技能树状图"""

    @functools.cached_property
    def _avatar_config_to_player_icon(self) -> dict[int, excel.AvatarPlayerIcon]:
        avatars: dict[int, excel.AvatarPlayerIcon] = {}
        for icon in self.avatar_player_icon():
            model = icon._excel  # pyright: ignore[reportPrivateUsage]
            avatars[model.avatar_id] = model
        return avatars

    @functools.cached_property
    def _avatar_config_skill_trees(self) -> dict[int, list[excel.AvatarSkillTreeConfig]]:
        skills: dict[int, list[excel.AvatarSkillTreeConfig]] = {}
        for skill in self.avatar_skill_tree_config():
            model = skill._excel  # pyright: ignore[reportPrivateUsage]
            if model.avatar_id not in skills:
                skills[model.avatar_id] = [model]
            else:
                skills[model.avatar_id].append(model)
        return skills

    @excel_output_main_sub(view.StoryAtlas)
    def story_atlas(self):
        """角色故事"""

    @excel_output_main_sub(view.VoiceAtlas)
    def voice_atlas(self):
        """角色语音"""

    ######## book ########

    @excel_output(view.BookDisplayType)
    def book_display_type(self):
        """"""

    @excel_output(view.BookSeriesConfig)
    def book_series_config(self):
        """阅读物系列"""

    @excel_output_name(view.BookSeriesConfig, book_series_config)
    def book_series_config_name(self):
        """阅读物系列"""

    @excel_output(view.BookSeriesWorld)
    def book_series_world(self):
        """阅读物所属的世界"""

    @excel_output(view.LocalbookConfig)
    def localbook_config(self):
        """每一卷阅读物"""

    @functools.cached_property
    def _book_series_localbook(self) -> dict[int, list[excel.LocalbookConfig]]:
        book_series: dict[int, list[excel.LocalbookConfig]] = {}
        for book in self.localbook_config():
            if book.series.id in book_series:
                book_series[book.series.id].append(book._excel)  # pyright: ignore[reportPrivateUsage]
            else:
                book_series[book.series.id] = [book._excel]  # pyright: ignore[reportPrivateUsage]
        return book_series

    ######## challenge ########

    @excel_output(view.ChallengeGroupConfig)
    def challenge_group_config(self):
        """混沌回忆单期"""

    @excel_output(view.ChallengeGroupConfig)
    def challenge_story_group_config(self):
        """虚构叙事单期"""

    @excel_output(view.ChallengeGroupConfig)
    def challenge_boss_group_config(self):
        """末日幻影单期"""

    @functools.cached_property
    def _challenge_group_mazes(self) -> dict[int, list[excel.ChallengeMazeConfig]]:
        """同属一期逐光捡金的层"""
        mazes: dict[int, list[excel.ChallengeMazeConfig]] = {}
        for maze in itertools.chain(
            self.challenge_maze_config(), self.challenge_story_maze_config(), self.challenge_boss_maze_config()
        ):
            model = maze._excel  # pyright: ignore[reportPrivateUsage]
            if model.group_id in mazes:
                mazes[model.group_id].append(model)
            else:
                mazes[model.group_id] = [model]
        return mazes

    @excel_output(view.ChallengeGroupExtra)
    def challenge_maze_group_extra(self):
        """混沌回忆单期额外数据（如增益列表、图标背景等）"""

    @excel_output(view.ChallengeStoryGroupExtra)
    def challenge_story_group_extra(self):
        """虚构叙事单期额外数据（如增益列表、图标背景等）"""

    @excel_output(view.ChallengeBossGroupExtra)
    def challenge_boss_group_extra(self):
        """末日幻影单期额外数据（如增益列表、图标背景等）"""

    @excel_output(view.ChallengeMazeConfig)
    def challenge_maze_config(self):
        """混沌回忆单层"""

    @excel_output(view.ChallengeMazeConfig)
    def challenge_story_maze_config(self):
        """虚构叙事单层"""

    @excel_output(view.ChallengeMazeConfig)
    def challenge_boss_maze_config(self):
        """末日幻影单层"""

    @excel_output(view.ChallengeStoryMazeExtra)
    def challenge_story_maze_extra(self):
        """虚构叙事单层额外数据（一波敌方数量等）"""

    @excel_output(view.ChallengeBossMazeExtra)
    def challenge_boss_maze_extra(self):
        """末日幻影单层（首领敌人）"""

    @excel_output(view.ScheduleData)
    def schedule_data_challenge_maze(self):
        """混沌回忆持续期间"""

    @excel_output(view.ScheduleData)
    def schedule_data_challenge_story(self):
        """虚构叙事持续期间"""

    @excel_output(view.ScheduleData)
    def schedule_data_challenge_boss(self):
        """末日幻影持续期间"""

    ######## fate ########
    # Fate 联动活动

    @excel_output(view.FateBuff)
    def fate_buff(self):
        """Fate 棋子"""

    @excel_output(view.FateHandbookMaster)
    def fate_handbook_master(self):
        """Fate 联动敌方从者图鉴"""

    @excel_output(view.FateMaster)
    def fate_master(self):
        """Fate 联动敌方从者"""

    @excel_output(view.FateMasterTalk)
    def fate_master_talk(self):
        """Fate 联动从者对话"""

    @excel_output_main_sub(view.MazeBuff)
    def fate_maze_buff(self):
        """Fate 棋子"""

    @excel_output(view.FateReiju)
    def fate_reiju(self):
        """Fate 令咒"""

    @excel_output(view.FateTrait)
    def fate_trait(self):
        """Fate 棋子组合增益"""

    @excel_output(view.FateTraitBuff)
    def fate_trait_buff(self):
        """Fate 棋子组合增益不同等级的效果"""

    ######## grid fight ########
    # 货币战争

    @excel_output(view.GridFightAugment)
    def grid_fight_augment(self):
        """货币战争投资策略"""

    @excel_output(view.GridFightBackRoleRank)
    def grid_fight_back_role_rank(self):
        """货币战争后台角色星魂效果"""

    @excel_output_main_sub(view.GridFightFrontSkill)
    def grid_fight_front_skill(self):
        """货币战争前台角色技能详情"""

    @excel_output(view.GridFightRoleBasicInfo)
    def grid_fight_role_basic_info(self):
        """货币战争角色"""

    @excel_output_main_sub(view.GridFightRoleSkillDisplay)
    def grid_fight_role_skill_display(self):
        """货币战争首页展示的技能方格，无详情"""

    @excel_output_main_sub(view.GridFightRoleStar)
    def grid_fight_role_star(self):
        """货币战争角色升星后属性变化"""

    @excel_output_string(view.GridFightRoleTagInfo)
    def grid_fight_role_tag_info(self):
        """货币战争角色 Tag（输出、辅助、奶妈、护盾）"""

    @excel_output(view.GridFightTraitBasicInfo)
    def grid_fight_trait_basic_info(self):
        """货币战争羁绊"""

    ######## hipplen ########

    @excel_output(view.ActivityHipplenTrait)
    def activity_hipplen_trait(self):
        """大地兽活动"""

    ######## item ########

    @excel_output(view.ItemConfig)
    def activity_item_config_avatar(self):
        """不清楚，看起来是活动试用角色？但是只有开拓者和三月七"""

    @excel_output(view.ItemConfig)
    def item_config(self):
        """道具"""

    @excel_output(view.ItemConfig)
    def item_config_avatar(self):
        """角色"""

    @excel_output(view.ItemConfig)
    def item_config_avatar_player_icon(self):
        """用户头像（角色自带）"""

    @excel_output(view.ItemConfig)
    def item_config_avatar_rank(self):
        """星魂"""

    @excel_output(view.ItemConfig)
    def item_config_avatar_skin(self):
        """时装"""

    @excel_output(view.ItemConfig)
    def item_config_book(self):
        """书籍"""

    @excel_output(view.ItemConfig)
    def item_config_disk(self):
        """碟片（音乐专辑）"""

    @excel_output(view.ItemConfig)
    def item_config_equipment(self):
        """光锥"""

    @excel_output(view.ItemConfig)
    def item_config_relic(self):
        """遗器"""

    @excel_output(view.ItemConfig)
    def item_config_train_dynamic(self):
        """"""

    @excel_output(view.ItemConfig)
    def item_player_card(self):
        """用户头像（时装、大月卡、活动、成就等头像）"""

    @excel_output(view.ItemCureInfoData)
    def item_cure_info_data(self):
        """道具可阅读内容"""

    @excel_output(view.ItemPurpose)
    def item_purpose(self):
        """
        道具子类型，展示在背包右上道具大图标的左上角
        和道具 SubType 高度相关
        """

    @excel_output(view.ItemUseData)
    def item_use_data(self):
        """道具使用奖励"""

    @typing.overload
    def item_config_all(self) -> collections.abc.Iterable[view.ItemConfig]: ...
    @typing.overload
    def item_config_all(self, id: int) -> view.ItemConfig | None: ...
    @typing.overload
    def item_config_all(self, id: collections.abc.Iterable[int]) -> collections.abc.Iterable[view.ItemConfig]: ...

    def item_config_all(
        self, id: int | collections.abc.Iterable[int] | None = None
    ) -> view.ItemConfig | collections.abc.Iterable[view.ItemConfig] | None:
        """从所有种类的 ItemConfig 中取得 ID 对应的那个"""
        methods = [
            self.item_config,
            self.item_config_avatar,
            self.item_config_avatar_player_icon,
            self.item_config_avatar_rank,
            self.item_config_avatar_skin,
            self.item_config_book,
            self.item_config_disk,
            self.item_config_equipment,
            self.item_config_relic,
            self.item_config_train_dynamic,
            self.item_player_card,
        ]
        if id is None:
            return itertools.chain.from_iterable(method() for method in methods)
        if isinstance(id, collections.abc.Iterable):
            return [next(filter(None, (method(item_id) for method in methods))) for item_id in id]
        return next(filter(None, (method(id) for method in methods)), None)

    ######## message ########

    @excel_output(view.EmojiConfig)
    def emoji_config(self):
        """表情"""

    @excel_output(view.EmojiGroup)
    def emoji_group(self):
        """表情包"""

    @excel_output(view.MessageContactsCamp)
    def message_contacts_camp(self):
        """联系人阵营"""

    @excel_output(view.MessageContactsConfig)
    def message_contacts_config(self):
        """联系人"""

    @excel_output(view.MessageContactsType)
    def message_contacts_type(self):
        """联系人类型（群聊、NPC、自机角色）"""

    @excel_output(view.MessageGroupConfig)
    def message_group_config(self):
        """联系人聊天记录（关联联系人和聊天记录）"""

    @excel_output(view.MessageItemConfig)
    def message_item_config(self):
        """聊天单条消息"""

    @excel_output(view.MessageItemImage)
    def message_item_image(self):
        """聊天单条消息中的图片"""

    @excel_output(view.MessageItemLink)
    def message_item_link(self):
        """聊天单条消息中的链接（只在绥园任务出现）"""

    @excel_output(view.MessageItemRaidEntrance)
    def message_item_raid_entrance(self):
        """聊天单条消息中的秘境任务（只在罗浮丹恒视角出现）"""

    @excel_output(view.MessageItemVideo)
    def message_item_video(self):
        """聊天单条消息中的视频（只在空间站冥火大公绑架案出现）"""

    @excel_output(view.MessageSectionConfig)
    def message_section_config(self):
        """一次聊天"""

    @functools.cached_property
    def _message_section_config_items(self) -> dict[int, list[excel.MessageItemConfig]]:
        items: dict[int, list[excel.MessageItemConfig]] = {}
        for item in self.message_item_config():
            if item.section_id is None:
                continue
            model = item._excel  # pyright: ignore[reportPrivateUsage]
            if item.section_id in items:
                items[item.section_id].append(model)
            else:
                items[item.section_id] = [model]
        return items

    @functools.cached_property
    def _message_contact_sections(self) -> dict[int, list[excel.MessageSectionConfig]]:
        result: dict[int, list[excel.MessageSectionConfig]] = {}
        for group in self.message_group_config():
            model = group._excel  # pyright: ignore[reportPrivateUsage]
            sections = [
                section._excel  # pyright: ignore[reportPrivateUsage]
                for section in self.message_section_config(model.message_section_id_list)
            ]
            if model.message_contacts_id in result:
                result[model.message_contacts_id].extend(sections)
            else:
                result[model.message_contacts_id] = sections
        return result

    @functools.cached_property
    def _message_section_contacts(self) -> dict[int, excel.MessageContactsConfig]:
        result: dict[int, excel.MessageContactsConfig] = {}
        for group in self.message_group_config():
            model = group._excel  # pyright: ignore[reportPrivateUsage]
            for section_id in model.message_section_id_list:
                assert section_id not in result
                contacts = self.message_contacts_config(model.message_contacts_id)
                assert contacts is not None
                result[section_id] = contacts._excel  # pyright: ignore[reportPrivateUsage]
        return result

    ######## misc ########

    @excel_output(view.ExtraEffectConfig)
    def extra_effect_config(self):
        """效果说明"""

    @functools.cached_property
    def _extra_effect_config_names(self) -> set[str]:
        return {effect.name for effect in self.extra_effect_config()}

    @excel_output(view.LoopCGConfig)
    def loop_cg_config(self):
        """剧情视频"""

    @excel_output_main_sub(view.MazeBuff)
    def maze_buff(self):
        """战斗助益（或增益），模拟宇宙祝福和逐光捡金效果都引用此"""

    @excel_output(view.RewardData)
    def reward_data(self):
        """奖励"""

    @excel_output(view.TextJoinConfig)
    def text_join_config(self):
        """"""

    @excel_output(view.TextJoinItem)
    def text_join_item(self):
        """"""

    def _text_join_config_item(self, id: int) -> tuple[int, list[str]]:
        config = self.text_join_config(id)
        if config is None:
            return 0, []
        default_item_index = [item.id for item in config.item_list].index(config.default_item.id)
        if default_item_index == -1:
            default_item_index = 1
        return default_item_index, [item.text for item in config.item_list]

    ######## mission ########

    @excel_output(view.ChronicleConclusion)
    def chronicle_conclusion(self):
        """命路歧途文案"""

    @excel_output(view.MainMission)
    def main_mission(self):
        """任务（会展示在任务列表里的内容）"""

    @excel_output(view.SubMission)
    def sub_mission(self):
        """子任务（某一小节，比如与某人对话、与敌人战斗）"""

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

    @excel_output_name(view.MonsterConfig, monster_config)
    def monster_config_name(self):
        """敌人详情"""

    @functools.cached_property
    def _monster_config_summoners(self) -> dict[int, list[excel.MonsterConfig]]:
        summoners: dict[int, list[excel.MonsterConfig]] = {}
        for monster in self.monster_config():
            model = monster._excel  # pyright: ignore[reportPrivateUsage]
            if model.summon_id_list is None:
                continue
            for summon in model.summon_id_list:
                if summon in summoners:
                    summoners[summon].append(model)
                else:
                    summoners[summon] = [model]
        return summoners

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
    def _monster_template_monster(self) -> dict[int, list[excel.MonsterConfig]]:
        monster_dict: dict[int, list[excel.MonsterConfig]] = {}
        for monster in self.monster_config():
            model = monster._excel  # pyright: ignore[reportPrivateUsage]
            if model.monster_template_id in monster_dict:
                monster_dict[model.monster_template_id].append(model)
            else:
                monster_dict[model.monster_template_id] = [model]
        return monster_dict

    @functools.cached_property
    def _monster_template_group(self) -> dict[int, list[excel.MonsterTemplateConfig]]:
        template_groups: dict[int, list[excel.MonsterTemplateConfig]] = {}
        for template in self.monster_template_config():
            group_id = template.group_id
            if group_id is None:
                continue
            if template_groups.get(group_id) is None:
                template_groups[group_id] = [template._excel]  # pyright: ignore[reportPrivateUsage]
            else:
                template_groups[group_id].append(template._excel)  # pyright: ignore[reportPrivateUsage]
        return template_groups

    @excel_output(view.NPCMonsterData)
    def npc_monster_data(self):
        """敌人详情"""

    ######## monster guide ########

    @excel_output(view.MonsterDifficultyGuide)
    def monster_difficulty_guide(self):
        """末日幻影首领特性"""

    @excel_output(view.MonsterGuideConfig)
    def monster_guide_config(self):
        """末日幻影内置攻略"""

    @excel_output(view.MonsterGuidePhase)
    def monster_guide_phase(self):
        """末日幻影应对策略"""

    @excel_output(view.MonsterGuideSkill)
    def monster_guide_skill(self):
        """末日幻影应对策略展开详情"""

    @excel_output(view.MonsterGuideSkillText)
    def monster_guide_skill_text(self):
        """末日幻影应对策略展开详情文案"""

    @excel_output(view.MonsterGuideTag)
    def monster_guide_tag(self):
        """末日幻影首领特性"""

    @excel_output(view.MonsterTextGuide)
    def monster_text_guide(self):
        """末日幻影挑战策略"""

    ######## performance ########

    @excel_output_string(view.CutSceneConfig)
    def cut_scene_config(self):
        """过场"""

    @excel_output(view.Performance)
    def performance_a(self):
        """剧情演出"""

    @excel_output(view.Performance)
    def performance_c(self):
        """剧情演出"""

    @excel_output(view.Performance)
    def performance_cg(self):
        """剧情演出"""

    @excel_output(view.Performance)
    def performance_d(self):
        """剧情演出"""

    @excel_output(view.Performance, "PerformanceDS")
    def performance_ds(self):
        """剧情演出"""

    @excel_output(view.Performance)
    def performance_e(self):
        """剧情演出"""

    @excel_output(view.Performance)
    def performance_video(self):
        """剧情演出"""

    @excel_output(view.VideoConfig)
    def video_config(self):
        """游戏内视频"""

    ######## planet fes ########
    # 二周年活动

    @excel_output(view.PlanetFesAvatar)
    def planet_fes_avatar(self):
        """3.2 二周年庆活动助理"""

    @excel_output(view.PlanetFesBuff)
    def planet_fes_avatar_buff(self):
        """3.2 二周年庆活动助理特质"""

    @excel_output(view.PlanetFesAvatarEvent)
    def planet_fes_avatar_event(self):
        """3.2 二周年庆活动访客事件"""

    @excel_output(view.PlanetFesAvatarEventOption)
    def planet_fes_avatar_event_option(self):
        """3.2 二周年庆活动访客事件选项"""

    @excel_output(view.PlanetFesAvatarLevel)
    def planet_fes_avatar_level(self):
        """3.2 二周年庆活动助理等级升级需要金币和升级后收入金币"""

    @excel_output(view.PlanetFesAvatarRarity)
    def planet_fes_avatar_rarity(self):
        """3.2 二周年庆活动助理工作技巧"""

    @excel_output(view.PlanetFesBuff)
    def planet_fes_buff(self):
        """3.2 二周年庆活动增益"""

    @excel_output_string(view.PlanetFesBuffType)
    def planet_fes_buff_type(self):
        """3.2 二周年庆活动增益类型（和描述）"""

    @excel_output(view.PlanetFesCard)
    def planet_fes_card(self):
        """3.2 二周年庆活动回忆卡"""

    @excel_output(view.PlanetFesCardTheme)
    def planet_fes_card_theme(self):
        """3.2 二周年庆活动回忆卡主题（阵营）"""

    @excel_output(view.PlanetFesFinishway)
    def planet_fes_finishway(self):
        """3.2 二周年庆活动参数列表"""

    @excel_output(view.PlanetFesGameReward)
    def planet_fes_game_reward(self):
        """3.2 二周年庆活动访客事件奖励"""

    @excel_output_main_sub(view.PlanetFesGameRewardPool)
    def planet_fes_game_reward_pool(self):
        """3.2 二周年庆活动访客事件奖励池"""

    @excel_output_string(view.PlanetFesLandType)
    def planet_fes_land_type(self):
        """3.2 二周年庆活动地块类型"""

    @excel_output(view.PlanetFesQuest)
    def planet_fes_quest(self):
        """3.2 二周年庆活动任务"""

    ######## rogue ########

    @excel_output(view.RogueBonus)
    def rogue_bonus(self):
        """模拟宇宙祝福"""

    @excel_output_main_sub(view.RogueBuff)
    def rogue_buff(self):
        """模拟宇宙祝福"""

    @excel_output_name(view.RogueBuff, rogue_buff)
    def rogue_buff_name(self):
        """模拟宇宙祝福"""

    @excel_output(view.RogueBuffGroup)
    def rogue_buff_group(self):
        """模拟宇宙祝福组，似乎是按 DLC 分类的"""

    @functools.cached_property
    def _rogue_buff_tag_groups(self) -> collections.defaultdict[int, list[excel.RogueBuffGroup]]:
        tag_to_group: collections.defaultdict[int, list[excel.RogueBuffGroup]] = collections.defaultdict(list)
        for group in self.rogue_buff_group():
            for tag in group.rogue_buff_drop:
                tag_to_group[tag].append(group._excel)  # pyright: ignore[reportPrivateUsage]
        return tag_to_group

    @functools.cached_property
    def _rogue_buff_tag_buff(self) -> dict[int, excel.RogueBuff]:
        tag_to_buff: dict[int, excel.RogueBuff] = {}
        for buff in self.rogue_buff():
            assert buff.tag not in tag_to_buff
            tag_to_buff[buff.tag] = buff._excel  # pyright: ignore[reportPrivateUsage]
        return tag_to_buff

    @excel_output(view.RogueBuffType)
    def rogue_buff_type(self):
        """模拟宇宙祝福命途（因为是模拟宇宙所以不包含同谐）"""

    @excel_output(view.RogueDialogueDynamicDisplay)
    def rogue_dialogue_dynamic_display(self):
        """模拟宇宙事件对话选项的展示 ID（暂时不明作用）"""

    @excel_output(view.RogueDialogueOptionDisplay)
    def rogue_dialogue_option_display(self):
        """模拟宇宙事件对话选项"""

    @excel_output(view.RogueEventSpecialOption)
    def rogue_event_special_option(self):
        """模拟宇宙事件特殊选项，如阮梅特殊选项、寰宇蝗灾命途选项等"""

    @excel_output(view.RogueHandBookEvent)
    def rogue_hand_book_event(self):
        """模拟宇宙事件图鉴信息"""

    @excel_output_name(view.RogueHandBookEvent, rogue_hand_book_event)
    def rogue_hand_book_event_name(self):
        """差分宇宙事件图鉴信息"""

    @excel_output(view.RogueHandBookEventType)
    def rogue_hand_book_event_type(self):
        """模拟宇宙事件图鉴所属模式、DLC"""

    @excel_output(view.RogueHandbookMiracle)
    def rogue_handbook_miracle(self):
        """模拟宇宙奇物图鉴信息（解锁奖励、在哪些 DLC 中出现等）"""

    @excel_output_name(view.RogueHandbookMiracle, rogue_handbook_miracle)
    def rogue_handbook_miracle_name(self):
        """模拟宇宙图鉴奇物（如「绝对失败处方」、「塔奥牌」等有不同效果的奇物故事等会出现于此）"""

    @functools.cached_property
    def _rogue_handbook_miracle_miracles(self) -> dict[int, list[excel.RogueMiracle]]:
        miracles: dict[int, list[excel.RogueMiracle]] = {}
        for miracle in itertools.chain(self.rogue_miracle(), self.rogue_magic_miracle()):
            model = miracle._excel  # pyright: ignore[reportPrivateUsage]
            if model.unlock_handbook_miracle_id is None:
                continue
            if model.unlock_handbook_miracle_id in miracles:
                miracles[model.unlock_handbook_miracle_id].append(model)
            else:
                miracles[model.unlock_handbook_miracle_id] = [model]
        return miracles

    @excel_output(view.RogueHandbookMiracleType)
    def rogue_handbook_miracle_type(self):
        """模拟宇宙奇物图鉴所属 DLC"""

    @excel_output_main_sub(view.MazeBuff)
    def rogue_maze_buff(self):
        """模拟、差分宇宙增益（可能来自祝福、奇物、方程、金血）"""

    @excel_output(view.RogueMiracle)
    def rogue_miracle(self):
        """模拟宇宙奇物"""

    @excel_output_name(view.RogueMiracle, rogue_miracle)
    def rogue_miracle_name():
        """模拟宇宙奇物"""

    @excel_output(view.RogueMiracleDisplay)
    def rogue_miracle_display(self):
        """模拟宇宙奇物效果"""

    @excel_output(view.RogueMiracleEffectDisplay)
    def rogue_miracle_effect_display(self):
        """模拟宇宙奇物效果"""

    @excel_output(view.RogueMonster)
    def rogue_monster(self):
        """模拟宇宙敌人"""

    @excel_output(view.RogueMonsterGroup)
    def rogue_monster_group(self):
        """为每个位面首领区域中可能出现的敌人"""

    @excel_output(view.RogueNPC)
    def rogue_npc(self):
        """模拟宇宙事件对应的配置文件"""

    @excel_output(view.RogueTalkNameConfig)
    def rogue_talk_name_config(self):
        """模拟宇宙事件对应的配置文件"""

    ######## rogue magic ########

    @excel_output(view.RogueMiracle)
    def rogue_magic_miracle(self):
        """不可知域奇物"""

    @excel_output_name(view.RogueMiracle, rogue_magic_miracle)
    def rogue_magic_miracle_name():
        """不可知域奇物"""

    @excel_output(view.RogueMiracleDisplay)
    def rogue_magic_miracle_display(self):
        """不可知域奇物效果"""

    @excel_output(view.RogueNPC)
    def rogue_magic_npc(self):
        """不可知域事件配置"""

    ######## rogue tourn ########

    @excel_output_main_sub(view.RogueTournBuff)
    def rogue_tourn_buff(self):
        """差分宇宙祝福"""

    @excel_output(view.RogueTournBuffGroup)
    def rogue_tourn_buff_group(self):
        """差分宇宙祝福组，似乎是按 TournMode 分类的"""

    @functools.cached_property
    def _rogue_tourn_buff_tag_groups(self) -> dict[int, list[excel.RogueTournBuffGroup]]:
        tag_to_group: dict[int, list[excel.RogueTournBuffGroup]] = {}
        for group in self.rogue_tourn_buff_group():
            for tag in group.rogue_buff_drop:
                model = group._excel  # pyright: ignore[reportPrivateUsage]
                if tag in tag_to_group:
                    tag_to_group[tag].append(model)
                else:
                    tag_to_group[tag] = [model]
        return tag_to_group

    @functools.cached_property
    def _rogue_tourn_buff_tag_buff(self) -> dict[int, excel.RogueTournBuff]:
        tag_to_buff: dict[int, excel.RogueTournBuff] = {}
        for buff in self.rogue_tourn_buff():
            assert buff.tag not in tag_to_buff
            tag_to_buff[buff.tag] = buff._excel  # pyright: ignore[reportPrivateUsage]
        return tag_to_buff

    @excel_output_name(view.RogueTournBuff, rogue_tourn_buff)
    def rogue_tourn_buff_name(self):
        """模拟宇宙祝福"""

    @excel_output(view.RogueTournBuffType)
    def rogue_tourn_buff_type(self):
        """差分宇宙祝福"""

    @excel_output(view.RogueTournFormula)
    def rogue_tourn_formula(self):
        """差分宇宙方程"""

    @excel_output(view.RogueTournFormulaDisplay)
    def rogue_tourn_formula_display(self):
        """差分宇宙方程效果"""

    @excel_output(view.RogueTournHandBookEvent)
    def rogue_tourn_hand_book_event(self):
        """差分宇宙事件图鉴信息"""

    @excel_output_name(view.RogueTournHandBookEvent, rogue_tourn_hand_book_event)
    def rogue_tourn_hand_book_event_name(self):
        """差分宇宙事件图鉴信息"""

    @excel_output(view.RogueTournHandbookMiracle)
    def rogue_tourn_handbook_miracle(self):
        """差分宇宙图鉴奇物（如「绝对失败处方」、「塔奥牌」等有不同效果的奇物故事等会出现于此）"""

    @excel_output_name(view.RogueTournHandbookMiracle, rogue_tourn_handbook_miracle)
    def rogue_tourn_handbook_miracle_name(self):
        """差分宇宙图鉴奇物（如「绝对失败处方」、「塔奥牌」等有不同效果的奇物故事等会出现于此）"""

    @functools.cached_property
    def _rogue_tourn_handbook_miracle_miracles(self) -> dict[int, list[excel.RogueTournMiracle]]:
        miracles: dict[int, list[excel.RogueTournMiracle]] = {}
        for miracle in self.rogue_tourn_miracle():
            model = miracle._excel  # pyright: ignore[reportPrivateUsage]
            if model.handbook_miracle_id is None:
                continue
            if model.handbook_miracle_id in miracles:
                miracles[model.handbook_miracle_id].append(model)
            else:
                miracles[model.handbook_miracle_id] = [model]
        return miracles

    @excel_output(view.RogueTournMiracle)
    def rogue_tourn_miracle(self):
        """差分宇宙奇物（如「天慧合金Ⅰ型」、「绝对失败处方」、「塔奥牌」等的具体奇物会各自分列于此）"""

    @excel_output_name(view.RogueTournMiracle, rogue_tourn_miracle)
    def rogue_tourn_miracle_name():
        """差分宇宙奇物"""

    @excel_output(view.RogueMiracleDisplay)
    def rogue_tourn_miracle_display(self):
        """差分宇宙奇物展示信息"""

    @excel_output(view.RogueNPC)
    def rogue_tourn_npc(self):
        """差分宇宙事件对应的配置文件"""

    @excel_output(view.RogueTournTitanBless)
    def rogue_tourn_titan_bless(self):
        """差分宇宙金血祝颂"""

    @excel_output(view.RogueTournWeeklyChallenge)
    def rogue_tourn_weekly_challenge(self):
        """差分宇宙周期演算"""

    @excel_output(view.RogueTournWeeklyDisplay)
    def rogue_tourn_weekly_display(self):
        """差分宇宙周期演算预设"""

    ######## stage ########

    @excel_output(view.StageConfig)
    def stage_config(self):
        """战斗波次信息"""

    @excel_output(view.StageInfiniteGroup)
    def stage_infinite_group(self):
        """战斗波次信息（目前已知虚构叙事波次信息在此）"""

    @excel_output(view.StageInfiniteMonsterGroup)
    def stage_infinite_monster_group(self):
        """战斗波次信息（目前已知虚构叙事波次信息在此）"""

    @excel_output(view.StageInfiniteWaveConfig)
    def stage_infinite_wave_config(self):
        """战斗波次信息（目前已知虚构叙事波次信息在此）"""

    ######## talk ########

    @excel_output(view.VoiceConfig)
    def voice_config(self):
        """语音"""

    @excel_output(view.TalkSentenceConfig)
    def talk_sentence_config(self):
        """各种对话，包括剧情、模拟宇宙事件等"""

    @excel_output(view.HeartDialTalk)
    def heart_dial_talk(self):
        """语音"""

    ######## tutorial ########

    @excel_output(view.TutorialGuideData)
    def tutorial_guide_data(self):
        """教学内容，单页"""

    @excel_output(view.TutorialGuideGroup)
    def tutorial_guide_group(self):
        """教学内容"""
