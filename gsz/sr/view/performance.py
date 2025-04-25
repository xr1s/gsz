from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc
    import pathlib

    from .. import act


class CutSceneConfig(View[excel.CutSceneConfig]):
    ExcelOutput: typing.Final = excel.CutSceneConfig

    @functools.cached_property
    def __captions(self) -> list[act.model.caption.CaptionSentence]:
        from .. import act

        if self._excel.caption_path == "":
            return []
        path = self._game.base.joinpath(self._excel.caption_path)
        caption = act.model.caption.Caption.model_validate_json(path.read_bytes())
        return caption.caption_list

    def captions(self) -> collections.abc.Iterable[act.CaptionSentence]:
        from .. import act

        return (act.CaptionSentence(self._game, caption) for caption in self.__captions)


class Performance(View[excel.Performance]):
    ExcelOutput: typing.Final = excel.Performance

    @property
    def path(self) -> pathlib.Path | None:
        if self._excel.performance_path == "":
            return None
        return self._game.base.joinpath(self._excel.performance_path.strip())

    @functools.cached_property
    def __performance(self) -> act.Act | None:
        from ..act import Act

        if self.path is None:
            return None
        if not self.path.is_file():
            return None
        return Act(self._game, self.path)

    def performance(self) -> act.Act | None:
        from .. import act

        return None if self.__performance is None else act.Act(self._game, self.__performance._act)  # pyright: ignore[reportPrivateUsage]


class VideoConfig(View[excel.VideoConfig]):
    ExcelOutput: typing.Final = excel.VideoConfig

    @functools.cached_property
    def __captions(self) -> list[act.model.caption.CaptionSentence]:
        from .. import act

        if self._excel.caption_path == "":
            return []
        path = self._game.base.joinpath(self._excel.caption_path)
        caption = act.model.caption.Caption.model_validate_json(path.read_bytes())
        return caption.caption_list

    def captions(self) -> collections.abc.Iterable[act.CaptionSentence]:
        from .. import act

        return (act.CaptionSentence(self._game, caption) for caption in self.__captions)

    @property
    def path(self) -> str:
        return self._excel.video_path
