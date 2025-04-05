import enum
import typing

import pydantic
import typing_extensions

from .base import Element, ModelID, ModelMainSubID, Text


class Type(enum.Enum):
    Memory = "Memory"
    """混沌回忆"""
    Story = "Story"
    """虚构叙事"""
    Boss = "Boss"
    """末日幻影"""


class ChallengeGroupConfig(ModelID):
    """逐光捡金"""

    group_id: int
    group_name: Text
    reward_line_group_id: int
    pre_mission_id: int
    global_schedule_id: int | None = None
    schedule_data_id: int | None = None
    maze_buff_id: int | None = None
    map_entrance_id: int | None = None
    mapping_info_id: int | None = None
    world_id: int | None = None
    back_ground_path: str | None = None
    tab_pic_path: str | None = None
    tab_pic_select_path: str | None = None
    challenge_group_type: Type = Type.Memory  # 1.5 及之前虚构叙事出现前，无此字段
    theme_pic_path: str | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.group_id


class StoryType(enum.Enum):
    Normal = "Normal"
    """
    1.6 版本首期到 2.6 版本的虚构叙事
    多波次怪物和增援，利好群攻多动角色
    按照之前的经验，每 3 期会轮换分别给终结技、DoT、追击类角色增益
    """
    Fever = "Fever"
    """
    2.7 新版虚构叙事
    新增「战意」机制，属于全局增益效果，替换此前的「怪诞逸闻」
    除此之外，每一轮都有首领，击败首领直接获得所有分数
    击败小怪也获得分数，并且首领扣除 3% 生命
    """


class ChallengeGroupExtra(ModelID):
    group_id: int
    theme_poster_bg_pic_path: typing.Annotated[str, pydantic.Field(alias="ThemePosterBgPicPath")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.group_id


class ChallengeGroupExtraTheme(ChallengeGroupExtra, ModelID):
    theme_toast_pic_path: str
    theme_icon_pic_path: str
    theme_poster_effect_prefab_path: str
    theme_poster_tab_pic_path: str


class ChallengeStoryGroupExtra(ChallengeGroupExtraTheme, ModelID):
    theme_id: int
    sub_maze_buff_list: list[int]  # 仅出现于 2.7 及之后
    story_type: StoryType = StoryType.Normal
    buff_list: list[int]


class ChallengeBossGroupExtra(ChallengeGroupExtraTheme, ModelID):
    buff_list_1: list[int]
    buff_list_2: list[int]
    boss_pattern_prefab_path: str
    boss_position_prefab_path_1: str
    boss_position_prefab_path_2: str


class ChallengeMazeConfig(ModelID):
    id_: int
    name: Text
    group_id: int
    map_entrance_id: int
    map_entrance_id_2: int | None = None
    pre_level: typing.Literal[1] | None = None
    pre_challenge_maze_id: int | None = None
    floor: int | None = None
    reward_id: int
    damage_type_1: list[Element]
    damage_type_2: list[Element]
    challenge_target_id: list[int]
    stage_num: int
    monster_id_1: list[int]
    monster_id_2: list[int]
    challenge_count_down: int | None = None  # 仅出现于混沌回忆
    maze_group_id_1: int
    config_list_1: list[int]
    npc_monster_id_lits_1: typing.Annotated[list[int], pydantic.Field(alias="NpcMonsterIDList1")]
    event_id_list_1: list[int]
    maze_group_id_2: int | None = None  # Option 是因为混沌回忆（入门级）没有下半场
    config_list_2: list[int]
    npc_monster_id_list_2: typing.Annotated[list[int], pydantic.Field(alias="NpcMonsterIDList2")]
    event_id_list_2: list[int]
    maze_buff_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class ChallengeStoryMazeExtra(ModelID):
    id_: int
    turn_limit: int
    battle_target_id: list[int]
    clear_score: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class ChallengeBossMazeExtra(ModelID):
    id_: int
    monster_id_1: int
    monster_id_2: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class ChallengeTargetType(enum.Enum):
    DeadAvatar = "DEAD_AVATAR"
    RoundsLeft = "ROUNDS_LEFT"
    TotalScore = "TOTAL_SCORE"


class ChallengeTargetConfig(ModelID):
    id_: int
    challenge_target_type: ChallengeTargetType
    challenge_target_name: Text
    challenge_target_param_1: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class RewardLine(ModelMainSubID):
    """每三星获得的奖励"""

    group_id: int
    star_count: int
    reward_id: int

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.group_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.star_count
