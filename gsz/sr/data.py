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

from . import view
from ..format import Formatter, Syntax

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
    def __get__(self, instance: "GameData", owner: type["GameData"]) -> GameDataMethod[T_co]: ...
    @typing.overload
    def __get__(self, instance: None, owner: type["GameData"]) -> "GameDataFunction[T_co]": ...
    @typing.overload
    def __call__(self, game: "GameData") -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, game: "GameData", id: int) -> T_co | None: ...
    @typing.overload
    def __call__(self, game: "GameData", id: collections.abc.Iterable[int]) -> collections.abc.Iterable[T_co]: ...


ABBR_WORDS = {"npc"}


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
        self.__excel_output: dict[int | None, excel.ModelID] | None = None

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
                    ExcelOutputDict = pydantic.TypeAdapter(dict[int | None, self.__type.ExcelOutput])
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
    def __get__(self, instance: "GameData", owner: type["GameData"]) -> GameDataMainSubMethod[T_co]: ...
    @typing.overload
    def __get__(self, instance: None, owner: type["GameData"]) -> "GameDataMainSubFunction[T_co]": ...
    @typing.overload
    def __call__(self, game: "GameData") -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, game: "GameData", main_id: int) -> collections.abc.Iterable[T_co]: ...
    @typing.overload
    def __call__(self, game: "GameData", main_id: int, sub_id: int) -> T_co | None: ...


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
                    return iter(()) if main_id is None or sub_id is None else None
                finally:
                    self.__file_names = ()  # 清理一下方便 GC
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

    def __init__(self, game: "GameData", excel: NE_co): ...

    @property
    def name(self) -> str: ...


class CachedPropertyName(typing.Protocol[NE_co]):
    _excel: NE_co

    def __init__(self, game: "GameData", excel: NE_co): ...

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

    def __call__(self, _method: typing.Callable[..., None]) -> typing.Callable[["GameData", str], list[NV]]:
        def fn(game: "GameData", name: str) -> list[NV]:
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
        candidates = iter(language.candidates())
        text_map_path = self.base / "TextMap" / f"TextMap{next(candidates)}.json"
        while not text_map_path.exists():
            text_map_path: pathlib.Path = self.base / "TextMap" / f"TextMap{next(candidates)}.json"
        text_map = text_map_path.read_bytes()
        self.__text_map = pydantic.TypeAdapter(dict[int, str]).validate_json(text_map)

    def text(self, text: "Text") -> str:
        return self.__text_map.get(text.hash, "")

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
        templates_path = self_path.parent.parent / "templates"
        env = jinja2.Environment(
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="${",
            variable_end_string="}",
            comment_start_string="%",
            loader=jinja2.FileSystemLoader(templates_path),
        )
        env.filters.update(gszformat=self._mw_formatter.format, gszformat_pretty=self._mw_pretty_formatter.format)
        return env

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

    @excel_output(view.ItemPurpose)
    def item_purpose(self):
        """道具目的"""

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

    ######## book ########

    @excel_output(view.BookDisplayType)
    def book_display_type(self):
        """"""

    @excel_output(view.BookSeriesConfig)
    def book_series_config(self):
        """阅读物系列"""

    @excel_output(view.BookSeriesWorld)
    def book_series_world(self):
        """阅读物所属的世界"""

    @excel_output(view.LocalbookConfig)
    def localbook_config(self):
        """每一卷阅读物"""

    @functools.cached_property
    def _book_series_localbook(self) -> dict[int, list["excel.LocalbookConfig"]]:
        book_series: dict[int, list[excel.LocalbookConfig]] = {}
        for book in self.localbook_config():
            if book.series.id in book_series:
                book_series[book.series.id].append(book._excel)  # pyright: ignore[reportPrivateUsage]
            else:
                book_series[book.series.id] = [book._excel]  # pyright: ignore[reportPrivateUsage]
        return book_series

    ######## misc ########

    @excel_output(view.ExtraEffectConfig)
    def extra_effect_config(self):
        """效果说明"""

    @functools.cached_property
    def _extra_effect_config_names(self) -> set[str]:
        return {effect.name for effect in self.extra_effect_config()}

    @excel_output(view.RewardData)
    def reward_data(self):
        """奖励"""

    @excel_output_main_sub(view.MazeBuff)
    def maze_buff(self):
        """战斗助益（或增益），模拟宇宙祝福和逐光捡金效果都引用此"""

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
    def _monster_template_group(self) -> dict[int, list["excel.MonsterTemplateConfig"]]:
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
    def __rogue_buff_tag_groups(self) -> collections.defaultdict[int, list["excel.RogueBuffGroup"]]:
        tag_to_group: collections.defaultdict[int, list[excel.RogueBuffGroup]] = collections.defaultdict(list)
        for group in self.rogue_buff_group():
            for tag in group.rogue_buff_drop:
                tag_to_group[tag].append(group._excel)  # pyright: ignore[reportPrivateUsage]
        return tag_to_group

    def rogue_buff_tag_groups(self, tag: int) -> list[view.RogueBuffGroup]:
        return [view.RogueBuffGroup(self, group) for group in self.__rogue_buff_tag_groups[tag]]

    @functools.cached_property
    def __rogue_buff_tag_buff(self) -> dict[int, "excel.RogueBuff"]:
        tag_to_buff: dict[int, excel.RogueBuff] = {}
        for buff in self.rogue_buff():
            assert buff.tag not in tag_to_buff
            tag_to_buff[buff.tag] = buff._excel  # pyright: ignore[reportPrivateUsage]
        return tag_to_buff

    def rogue_buff_tag_buff(self, tag: int) -> view.RogueBuff | None:
        buff = self.__rogue_buff_tag_buff.get(tag)
        return None if buff is None else view.RogueBuff(self, buff)

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
    def __rogue_handbook_miracle_miracles(self) -> dict[int, list["excel.RogueMiracle"]]:
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

    def rogue_handbook_miracle_miracles(self, handbook_miracle_id: int) -> collections.abc.Iterable[view.RogueMiracle]:
        miracles = self.__rogue_handbook_miracle_miracles.get(handbook_miracle_id, ())
        return (view.RogueMiracle(self, miracle) for miracle in miracles)

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

    ######## rogue_magic ########

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

    ######## rogue_tourn ########

    @excel_output_main_sub(view.RogueTournBuff)
    def rogue_tourn_buff(self):
        """差分宇宙祝福"""

    @excel_output(view.RogueTournBuffGroup)
    def rogue_tourn_buff_group(self):
        """差分宇宙祝福组，似乎是按 TournMode 分类的"""

    @functools.cached_property
    def __rogue_tourn_buff_tag_groups(self) -> dict[int, list["excel.RogueTournBuffGroup"]]:
        tag_to_group: collections.defaultdict[int, list[excel.RogueTournBuffGroup]] = collections.defaultdict(list)
        for group in self.rogue_tourn_buff_group():
            for tag in group.rogue_buff_drop:
                tag_to_group[tag].append(group._excel)  # pyright: ignore[reportPrivateUsage]
        return tag_to_group

    def rogue_tourn_buff_tag_groups(self, tag: int) -> list[view.RogueTournBuffGroup]:
        return [view.RogueTournBuffGroup(self, group) for group in self.__rogue_tourn_buff_tag_groups[tag]]

    @functools.cached_property
    def __rogue_tourn_buff_tag_buff(self) -> dict[int, "excel.RogueTournBuff"]:
        tag_to_buff: dict[int, excel.RogueTournBuff] = {}
        for buff in self.rogue_tourn_buff():
            assert buff.tag not in tag_to_buff
            tag_to_buff[buff.tag] = buff._excel  # pyright: ignore[reportPrivateUsage]
        return tag_to_buff

    def rogue_tourn_buff_tag_buff(self, tag: int) -> view.RogueTournBuff | None:
        buff = self.__rogue_tourn_buff_tag_buff.get(tag)
        return None if buff is None else view.RogueTournBuff(self, buff)

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
    def __rogue_tourn_handbook_miracle_miracles(self) -> dict[int, list["excel.RogueTournMiracle"]]:
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

    def rogue_tourn_handbook_miracle_miracles(
        self, handbook_miracle_id: int
    ) -> collections.abc.Iterable[view.RogueTournMiracle]:
        miracles = self.__rogue_tourn_handbook_miracle_miracles.get(handbook_miracle_id, ())
        return (view.RogueTournMiracle(self, miracle) for miracle in miracles)

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

    ######## talk ########
    @excel_output(view.TalkSentenceConfig)
    def talk_sentence_config(self):
        """各种对话，包括剧情、模拟宇宙事件等"""

    @excel_output(view.VoiceConfig)
    def voice_config(self):
        """语音"""
