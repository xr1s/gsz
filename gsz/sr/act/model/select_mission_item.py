from .base import BaseModel


class ItemSelect(BaseModel):
    item_1: int
    item_2: int | None = None
    trigger_custom_string: str


class SimpleTalk(BaseModel):
    talk_sentence_id: int | None = None
