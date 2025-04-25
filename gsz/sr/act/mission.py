from __future__ import annotations

import functools
import pathlib
import typing

from . import act, model

if typing.TYPE_CHECKING:
    from ..data import GameData


class MissionInfo:
    def __init__(self, game: GameData, mission: model.MissionInfo | pathlib.Path):
        self._game: GameData = game
        self._mission: model.MissionInfo = (
            mission
            if isinstance(mission, model.MissionInfo)
            else model.MissionInfo.model_validate_json(game.base.joinpath(mission).read_bytes())
        )

    def sub_missions(self) -> list[SubMission]:
        return [SubMission(self._game, sub) for sub in self._mission.sub_mission_list]


class SubMission:
    def __init__(self, game: GameData, mission: model.mission.SubMission):
        self._game: GameData = game
        self._mission: model.mission.SubMission = mission

    @functools.cached_property
    def __act(self) -> model.act.Act | None:
        if self._mission.mission_json_path is None:
            return None
        path = pathlib.Path(self._game.base.joinpath(self._mission.mission_json_path))
        return model.act.Act.model_validate_json(path.read_bytes())

    def act(self) -> act.Act | None:
        return None if self.__act is None else act.Act(self._game, self.__act)
