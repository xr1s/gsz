from __future__ import annotations

import functools
import typing

import typing_extensions

from . import model
from .wiki import Dialogue

if typing.TYPE_CHECKING:
    import collections.abc
    import pathlib

    from ..data import GameData
    from .sequence import Sequence
    from .task import Task


class Act(Dialogue):
    def __init__(self, game: GameData, excel: pathlib.Path | model.Act):
        self._game: GameData = game
        self._act: model.Act = (
            excel
            if isinstance(excel, model.Act)
            else model.Act.model_validate_json(game.base.joinpath(excel).read_bytes())
        )

    @functools.cached_property
    def __tasks(self) -> list[model.Task]:
        if self._act.on_start_sequece is None:
            return []
        return [task for seq in self._act.on_start_sequece if seq.task_list is not None for task in seq.task_list]

    def tasks(self) -> collections.abc.Iterable[Task]:
        from .task import Task

        return (Task(self._game, task) for task in self.__tasks)

    def on_start_sequence(self) -> collections.abc.Iterable[Sequence]:
        from .sequence import Sequence

        if self._act.on_start_sequece is None:
            return ()
        return (Sequence(self._game, seq, index) for index, seq in enumerate(self._act.on_start_sequece))

    @functools.cached_property
    @typing_extensions.override
    def _sequences(self) -> list[Sequence]:
        from .sequence import Sequence

        if self._act.on_start_sequece is None:
            return []
        return [Sequence(self._game, seq, index) for index, seq in enumerate(self._act.on_start_sequece)]
