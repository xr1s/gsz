from __future__ import annotations

import functools
import typing

from ..excel import Value
from . import model
from .task import Task

if typing.TYPE_CHECKING:
    import collections.abc

    from ..data import GameData


class Sequence:
    def __init__(self, game: GameData, excel: model.Sequence, index: int):
        self._game: GameData = game
        self._seq: model.Sequence = excel
        self.successors: list[Sequence] | None = None
        self.confluence: Sequence | None = None
        self.index: int = index

    def tasks(self) -> collections.abc.Iterable[Task]:
        return (Task(self._game, task) for task in self._seq.task_list or ())

    @functools.cached_property
    def wait_custom_string(self) -> str:
        if self._seq.task_list is None:
            return ""
        for task in self._seq.task_list:
            if not isinstance(task, model.task.WaitCustomString):
                return ""
            if not isinstance(task.custom_string, Value):
                return ""
            return task.custom_string.value
        return ""

    @staticmethod
    def __trigger_custom_string(tasks: list[model.Task]) -> list[str]:  # noqa: PLR0911
        for task in tasks:
            if isinstance(task, model.task.TriggerCustomString | model.task.TriggerCustomStringOnDialogEnd):
                return [] if isinstance(task.custom_string, model.Custom) else [task.custom_string.value]
            if isinstance(task, model.task.PlayOptionTalk):
                if task.trigger_string is not None:
                    # 这种情况一般是 Loop
                    # Loop 中每个选项有一个自己的 CustomString，会通向自己的分支剧情
                    # Loop 结束（选项全选过了）则会触发这里的 TriggerString
                    return [task.trigger_string]
                return [
                    option.trigger_custom_string
                    for option in task.option_list
                    if option.trigger_custom_string is not None
                ]
            if isinstance(task, model.task.PlayRogueOptionTalk):
                return [
                    option.trigger_custom_string
                    for option in task.option_list
                    if option.trigger_custom_string is not None
                ]
            if isinstance(task, model.task.PredicateTaskList):
                strings: list[str] = []
                if task.success_task_list is not None:
                    strings.extend(Sequence.__trigger_custom_string(task.success_task_list))
                if task.failed_task_list is not None:
                    strings.extend(Sequence.__trigger_custom_string(task.failed_task_list))
                return strings
            if isinstance(task, model.task.WaitDialogueEvent):
                return [
                    typing.cast(str, event.success_custom_string or event.failure_custom_string)
                    for event in task.dialogue_event_list
                ]
        return []

    @functools.cached_property
    def trigger_custom_string(self) -> list[str]:
        if self._seq.task_list is None:
            return []
        return self.__trigger_custom_string(self._seq.task_list)

    @functools.cached_property
    def is_entrypoint(self) -> bool:
        if self._seq.task_list is None:
            return False
        return any(
            isinstance(
                task,
                model.task.ShowRogueTalkUI | model.task.LevelPerformanceInitialize | model.task.CollectDataConditions,
            )
            for task in self._seq.task_list
        )

    @functools.cached_property
    def is_leavepoint(self) -> bool:
        if self._seq.task_list is None:
            return False
        return any(
            isinstance(task, model.task.EndPerformance | model.task.WaitPerformanceEnd) for task in self._seq.task_list
        )

    @functools.cached_property
    def is_wait_event(self) -> bool:
        if self._seq.task_list is None:
            return False
        return any(
            isinstance(task, model.task.WaitCustomString | model.task.WaitDialogueEvent) for task in self._seq.task_list
        )
