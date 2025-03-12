import collections.abc
import enum
import typing

import pydantic

from .base import ModelID, Text, Value


class ExtraEffectConfig(ModelID):
    """效果说明。游戏界面中文字上一般会有【】配合下划线装饰，点击会弹出全屏遮罩，遮罩上是名词的详细介绍"""

    extra_effect_id: int
    extra_effect_name: Text
    extra_effect_desc: Text
    desc_param_list: list[Value[float]]
    extra_effect_icon_path: str
    extra_effect_type: typing.Literal[1, 2, 3]  # 目前只有 1, 2, 3，从对应的描述上看 1 3 都是开发用数据，不露出

    @property
    @typing.override
    def id(self) -> int:
        return self.extra_effect_id


class RewardData(ModelID):
    reward_id: int
    hcoin: int | None = None
    item_id: list[int] | None = None
    count: list[int] | None = None
    level: list[typing.Literal[1] | None] | None = None
    rank: list[typing.Literal[1] | None] | None = None

    @property
    @typing.override
    def id(self) -> int:
        return self.reward_id

    @pydantic.model_validator(mode="before")
    @classmethod
    def model_serializer(cls, data: typing.Any) -> typing.Any:
        class RewardData(typing.TypedDict, total=False):
            RewardID: int
            Hcoin: int | None
            ItemID: collections.abc.Sequence[int | None] | None
            Count: collections.abc.Sequence[int | None] | None
            Level: collections.abc.Sequence[int | None] | None
            Rank: collections.abc.Sequence[int | None] | None

        def field(
            returns: RewardData,
            name: typing.Literal["ItemID", "Count", "Level", "Rank"],
            pos: list[tuple[int, int]],
        ):
            if len(pos) == 0:
                return
            items: list[int | None] = [None] * max(pos)[0]
            for index, item in pos:
                items[index - 1] = item
            returns[name] = items

        if not isinstance(data, dict):
            raise TypeError(f"RewardData must be dict, {data}")
        data = typing.cast(dict[str, int], data)
        item_id_pos: list[tuple[int, int]] | None = []
        count_pos: list[tuple[int, int]] | None = []
        level_pos: list[tuple[int, int]] | None = []
        rank_pos: list[tuple[int, int]] | None = []
        returns: RewardData = {}
        for key, val in data.items():
            if key in ("RewardID", "Hcoin"):
                returns[key] = val
            elif key.startswith("ItemID_"):
                item_id_pos.append((int(key[7:]), val))
            elif key.startswith("Count_"):
                count_pos.append((int(key[6:]), val))
            elif key.startswith("Level_"):
                level_pos.append((int(key[6:]), val))
            elif key.startswith("Rank_"):
                rank_pos.append((int(key[5:]), val))
        field(returns, "ItemID", item_id_pos)
        field(returns, "Count", count_pos)
        field(returns, "Level", level_pos)
        field(returns, "Rank", rank_pos)
        return returns


class TextJoinType(enum.Enum):
    AvatarID = "AvatarID"
    CustomText = "CustomText"


class TextJoinConfig(ModelID):
    text_join_id: int
    default_item: int
    text_join_item_list: list[int]
    is_override: bool = False
    type: TextJoinType | None = None

    @property
    @typing.override
    def id(self) -> int:
        return self.text_join_id


class TextJoinItem(ModelID):
    text_join_item_id: int
    text_join_text: Text | None = None

    @property
    @typing.override
    def id(self) -> int:
        return self.text_join_item_id
