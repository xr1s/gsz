import enum
import typing

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
