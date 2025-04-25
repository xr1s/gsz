import enum
import typing

import pydantic

from ...excel import Value
from .base import BaseModel, Custom, Dynamic, Empty, FixedValue, Model, get_discriminator


def get_fetch_type(v: typing.Any) -> str:
    if isinstance(v, dict):
        fetch_type = typing.cast(str | None, v.get("FetchType"))  # pyright: ignore[reportUnknownMemberType]
        return "" if fetch_type is None else fetch_type
    return v.fetch_type


class EntityType(enum.Enum):
    Anchor = "Anchor"
    LocalPlayer = "LocalPlayer"
    NPC = "NPC"
    NPCMonster = "NPCMonster"
    Prop = "Prop"


class GroupFetchLocalTarget(Model):
    target_type: typing.Literal["Prop"] | None = None
    targets: list[int] | None = None


class TargetAlias(Model):
    alias: typing.Literal["Caster", "LightTeamEntity"]


class TargetConcat(Model):
    targets: list["Target"]


class TargetFetchAdvLocalPlayer(Model):
    include_story_player: bool = True


class MonsterID(BaseModel):
    group_id: FixedValue[int]
    id: FixedValue[int]


class TargetFetchAdvMonsterExEmpty(Model):
    pass


class TargetFetchAdvMonsterExMultiByMonsterID(Model):
    fetch_type: typing.Literal["MultiByMonsterID"]
    multi_monster_id: list[MonsterID]


class TargetFetchAdvMonsterExSingleByMonsterID(Model):
    fetch_type: typing.Literal["SingleByMonsterID"]
    single_monster_id: MonsterID


TargetFetchAdvMonsterEx = typing.Annotated[
    typing.Annotated[TargetFetchAdvMonsterExEmpty, pydantic.Tag("")]
    | typing.Annotated[TargetFetchAdvMonsterExMultiByMonsterID, pydantic.Tag("MultiByMonsterID")]
    | typing.Annotated[TargetFetchAdvMonsterExSingleByMonsterID, pydantic.Tag("SingleByMonsterID")],
    pydantic.Discriminator(get_fetch_type),
]


class TargetFetchAdvNPC(Model):
    class NPCID(BaseModel):
        group_id: int
        group_npc_id: int

    multi_group_fetch: list[NPCID]


class NpcID(BaseModel):
    group_id: FixedValue[int] | None = None
    group_npc_id: FixedValue[int] | None = None


class TargetFetchAdvNpcExEmpty(Model):
    npc_id_in_owner_group: FixedValue[int] | None = None
    single_npc_key: Custom | None = None
    single_npc_id: NpcID | None = None
    single_unique_name: Value[str] | None = None


class TargetFetchAdvNpcExSingleNpcByNpcID(Model):
    fetch_type: typing.Literal["SingleNpcByNpcID"]
    single_npc_key: Custom | None = None
    single_npc_id: NpcID
    single_unique_name: Value[str] | None = None
    npc_id_in_owner_group: FixedValue[int] | None = None


class TargetFetchAdvNpcExSingleNpcByNpcKey(Model):
    fetch_type: typing.Literal["SingleNpcByNpcKey"]
    single_npc_key: Custom
    single_npc_id: NpcID | None = None
    single_unique_name: Value[str] | Custom | None = None


class TargetFetchAdvNpcExSingleNpcByOwnerGroupAndID(Model):
    fetch_type: typing.Literal["SingleNpcByOwnerGroupAndID"]
    single_npc_key: Custom | None = None
    single_npc_id: NpcID | None = None
    single_unique_name: Value[str] | None = None
    npc_id_in_owner_group: FixedValue[int]


class TargetFetchAdvNpcExSingleNpcByUniqueName(Model):
    fetch_type: typing.Literal["SingleNpcByUniqueName"]
    single_npc_id: NpcID | None = None
    single_unique_name: Value[str] | Custom


TargetFetchAdvNpcEx = typing.Annotated[
    typing.Annotated[TargetFetchAdvNpcExEmpty, pydantic.Tag("")]
    | typing.Annotated[TargetFetchAdvNpcExSingleNpcByNpcID, pydantic.Tag("SingleNpcByNpcID")]
    | typing.Annotated[TargetFetchAdvNpcExSingleNpcByNpcKey, pydantic.Tag("SingleNpcByNpcKey")]
    | typing.Annotated[TargetFetchAdvNpcExSingleNpcByOwnerGroupAndID, pydantic.Tag("SingleNpcByOwnerGroupAndID")]
    | typing.Annotated[TargetFetchAdvNpcExSingleNpcByUniqueName, pydantic.Tag("SingleNpcByUniqueName")],
    pydantic.Discriminator(get_fetch_type),
]


class PropID(BaseModel):
    group_id: FixedValue[int] | Dynamic | None = None
    id: FixedValue[int] | Dynamic | None = None


class TargetFetchAdvProp(Model):
    target_is_owner: bool = False
    multi_group_fetch: list[PropID]
    multi_group_fetch_by_unique_name: list[None] | None = None
    multi_group_fetch_by_prop_key: list[None] | None = None


class TargetFetchAdvPropExEmpty(Model):
    multi_prop_key: list[None] | None = None
    prop_id_in_owner_group: FixedValue[int] | None = None
    single_prop_key: Custom | None = None
    single_prop_id: PropID | None = None
    multi_prop_id: list[None] | None = None


class TargetFetchAdvPropExMultiPropByGroup(Model):
    fetch_type: typing.Literal["MultiPropByGroup"]
    single_prop_id: Empty | None = None
    prop_group: FixedValue[int]


class TargetFetchAdvPropExMultiPropByID(Model):
    fetch_type: typing.Literal["MultiPropByPropID"]
    multi_prop_id: list[PropID]


class TargetFetchAdvPropExSinglePropByOwnerGroupAndID(Model):
    fetch_type: typing.Literal["SinglePropByOwnerGroupAndID"]
    single_prop_id: PropID | None = None
    prop_id_in_owner_group: FixedValue[int]


class TargetFetchAdvPropExSinglePropByPropID(Model):
    fetch_type: typing.Literal["SinglePropByPropID"]
    single_prop_key: Custom | None = None
    single_prop_id: PropID
    multi_prop_key: list[None] | None = None
    prop_group: FixedValue[int] | None = None
    multi_prop_id: list[PropID] | None = None
    prop_id_in_owner_group: FixedValue[int] | None = None


class TargetFetchAdvPropExSinglePropByPropKey(Model):
    fetch_type: typing.Literal["SinglePropByPropKey"]
    single_prop_key: Custom
    prop_id_in_owner_group: FixedValue[typing.Literal[300003]] | None = None
    single_prop_id: PropID | None = None
    single_unique_name: Value[typing.Literal["30-300001"]] | None = None
    multi_prop_id: list[None] | None = None
    multi_prop_key: list[None] | None = None


TargetFetchAdvPropEx = typing.Annotated[
    typing.Annotated[TargetFetchAdvPropExEmpty, pydantic.Tag("")]
    | typing.Annotated[TargetFetchAdvPropExMultiPropByGroup, pydantic.Tag("MultiPropByGroup")]
    | typing.Annotated[TargetFetchAdvPropExMultiPropByID, pydantic.Tag("MultiPropByPropID")]
    | typing.Annotated[TargetFetchAdvPropExSinglePropByOwnerGroupAndID, pydantic.Tag("SinglePropByOwnerGroupAndID")]
    | typing.Annotated[TargetFetchAdvPropExSinglePropByPropID, pydantic.Tag("SinglePropByPropID")]
    | typing.Annotated[TargetFetchAdvPropExSinglePropByPropKey, pydantic.Tag("SinglePropByPropKey")],
    pydantic.Discriminator(get_fetch_type),
]


class TargetFetchAnchor(Model):
    group_id: int
    group_instance_id: int


class TargetFetchAnchorByName(Model):
    anchor_name: Custom


class TargetFetchCurrentGroupNPCMonsters(Model):
    pass


class TargetFetchDialogueEntity(Model):
    pass


class TargetFetchNormalPam(Model):
    pass


class TargetFetchOwnerEntity(Model):
    pass


class TargetFetchSummonUnit(Model):
    summoner: "Target"
    summon_unit_id: int | None = None


class TargetFetchUniqueName(Model):
    unique_name: str


class TargetFetchUniqueNameEntity(Model):
    unique_name: str


Target = typing.Annotated[
    typing.Annotated[GroupFetchLocalTarget, pydantic.Tag("GroupFetchLocalTarget")]
    | typing.Annotated[TargetAlias, pydantic.Tag("TargetAlias")]
    | typing.Annotated[TargetConcat, pydantic.Tag("TargetConcat")]
    | typing.Annotated[TargetFetchAdvLocalPlayer, pydantic.Tag("TargetFetchAdvLocalPlayer")]
    | typing.Annotated[TargetFetchAdvMonsterEx, pydantic.Tag("TargetFetchAdvMonsterEx")]
    | typing.Annotated[TargetFetchAdvNPC, pydantic.Tag("TargetFetchAdvNPC")]
    | typing.Annotated[TargetFetchAdvNpcEx, pydantic.Tag("TargetFetchAdvNpcEx")]
    | typing.Annotated[TargetFetchAdvProp, pydantic.Tag("TargetFetchAdvProp")]
    | typing.Annotated[TargetFetchAdvPropEx, pydantic.Tag("TargetFetchAdvPropEx")]
    | typing.Annotated[TargetFetchAnchor, pydantic.Tag("TargetFetchAnchor")]
    | typing.Annotated[TargetFetchAnchorByName, pydantic.Tag("TargetFetchAnchorByName")]
    | typing.Annotated[TargetFetchCurrentGroupNPCMonsters, pydantic.Tag("TargetFetchCurrentGroupNPCMonsters")]
    | typing.Annotated[TargetFetchDialogueEntity, pydantic.Tag("TargetFetchDialogueEntity")]
    | typing.Annotated[TargetFetchNormalPam, pydantic.Tag("TargetFetchNormalPam")]
    | typing.Annotated[TargetFetchOwnerEntity, pydantic.Tag("TargetFetchOwnerEntity")]
    | typing.Annotated[TargetFetchSummonUnit, pydantic.Tag("TargetFetchOwnerSummonUnit")]
    | typing.Annotated[TargetFetchUniqueName, pydantic.Tag("TargetFetchUniqueName")]
    | typing.Annotated[TargetFetchUniqueNameEntity, pydantic.Tag("TargetFetchUniqueNameEntity")],
    pydantic.Discriminator(get_discriminator),
]
