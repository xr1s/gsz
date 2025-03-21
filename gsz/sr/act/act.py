import typing

from .base import Model
from .task import Task
from .value import ValueSource


class Sequence(Model):
    is_loop: bool = False
    order: int | None = None
    task_list: list[Task]


class Act(Model):
    on_start_sequece: list[Sequence]
    on_init_sequece: list[Sequence] | None = None
    type: typing.Literal["PerformanceD"] | None = None
    value_source: ValueSource | None = None
