import enum

from .base import BaseModel
from .task import Task
from .value import ValueSource


class Sequence(BaseModel):
    is_loop: bool = False
    order: int | None = None
    task_list: list[Task] | None = None


class EntityEvent(BaseModel):
    name: str
    description: str
    is_client: bool = True
    is_private: bool = False


class Type(enum.Enum):
    Entity = "Entity"
    EntityInstance = "EntityInstance"
    Group = "Group"
    Mission = "Mission"
    PerformanceC = "PerformanceC"
    PerformanceD = "PerformanceD"
    SubGraph = "SubGraph"


class Act(BaseModel):
    on_start_sequece: list[Sequence] | None = None
    on_init_sequece: list[Sequence] | None = None
    value_source: ValueSource | None = None
    type: Type | None = None
    option_list: list[None] | None = None
    entity_event_list: list[EntityEvent] | None = None
