"""绳网"""

from __future__ import annotations

import functools
import typing

from .. import filecfg
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc


class InterKnotConfig(View[filecfg.InterKnotConfig]):
    FileCfg: typing.Final = filecfg.InterKnotConfig

    @functools.cached_property
    def poster(self) -> str:
        return self._game.text(self._filecfg.poster)

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._filecfg.title)

    @functools.cached_property
    def text(self) -> str:
        return self._game.text(self._filecfg.text)

    @functools.cached_property
    def __comments(self) -> list[filecfg.PostCommentConfig]:
        return self._game._comments_under_post.get(self._filecfg.comment_group, [])  # pyright: ignore[reportPrivateUsage]

    def comments(self) -> collections.abc.Iterable[PostCommentConfig]:
        return (PostCommentConfig(self._game, comment) for comment in self.__comments)

    @functools.cached_property
    def post_script(self) -> str:
        return self._game.text(self._filecfg.script)

    @functools.cached_property
    def replies(self) -> tuple[str, str] | None:
        if self._filecfg.reply_1 == "" and self._filecfg.reply_2 == "":
            return None
        reply_1 = self._game.text(self._filecfg.reply_1)
        reply_2 = self._game.text(self._filecfg.reply_2)
        if reply_1 == "" and reply_2 == "":
            return None
        return reply_1, reply_2

    @property
    def same_subsequent(self) -> bool:
        return self._filecfg.subsequent_1 == self._filecfg.subsequent_2

    @functools.cached_property
    def __subsequent(self) -> tuple[list[filecfg.PostCommentConfig], list[filecfg.PostCommentConfig]] | None:
        if self._filecfg.subsequent_1 == 0 and self._filecfg.subsequent_2 == 0:
            return None
        comments_under_post = self._game._comments_under_post  # pyright: ignore[reportPrivateUsage]
        subsequent_1 = comments_under_post.get(self._filecfg.subsequent_1, [])
        if self.same_subsequent:
            subsequent_2 = subsequent_1
        elif self._filecfg.subsequent_2 == 0:
            subsequent_2 = []
        else:
            subsequent_2 = comments_under_post.get(self._filecfg.subsequent_2, [])
        if len(subsequent_1) == 0 and len(subsequent_2) == 0:
            return None
        return subsequent_1, subsequent_2

    def subsequent(self) -> tuple[list[PostCommentConfig], list[PostCommentConfig]] | None:
        if self.__subsequent is None:
            return None
        subsequent_1 = [PostCommentConfig(self._game, comment) for comment in self.__subsequent[0]]
        if self.same_subsequent:
            return subsequent_1, subsequent_1
        return subsequent_1, [PostCommentConfig(self._game, comment) for comment in self.__subsequent[1]]


class PostCommentConfig(View[filecfg.PostCommentConfig]):
    FileCfg: typing.Final = filecfg.PostCommentConfig

    @functools.cached_property
    def commentator(self) -> str:
        return self._game.text(self._filecfg.commentator)

    @functools.cached_property
    def text(self) -> str:
        return self._game.text(self._filecfg.text)
