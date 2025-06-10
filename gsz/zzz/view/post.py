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

    @property
    def id(self) -> int:
        return self._filecfg.id_

    @functools.cached_property
    def poster(self) -> str:
        return self._game.text(self._filecfg.poster)

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._filecfg.title)

    @functools.cached_property
    def text(self) -> str:
        return self._game.text(self._filecfg.text)

    @property
    def image(self) -> str:
        return self._filecfg.image

    @functools.cached_property
    def __comments(self) -> list[filecfg.PostCommentConfig]:
        return self._game._comments_under_post.get(self._filecfg.comment_id, [])  # pyright: ignore[reportPrivateUsage]

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
    def same_follow_up(self) -> bool:
        return self._filecfg.follow_up_1 == self._filecfg.follow_up_2

    @functools.cached_property
    def __follow_up(self) -> tuple[list[filecfg.PostCommentConfig], list[filecfg.PostCommentConfig]] | None:
        if self._filecfg.follow_up_1 == 0 and self._filecfg.follow_up_2 == 0:
            return None
        comments_under_post = self._game._comments_under_post  # pyright: ignore[reportPrivateUsage]
        follow_up_1 = comments_under_post.get(self._filecfg.follow_up_1, [])
        if self.same_follow_up:
            follow_up_2 = follow_up_1
        elif self._filecfg.follow_up_2 == 0:
            follow_up_2 = []
        else:
            follow_up_2 = comments_under_post.get(self._filecfg.follow_up_2, [])
        if len(follow_up_1) == 0 and len(follow_up_2) == 0:
            return None
        return follow_up_1, follow_up_2

    def follow_up(self) -> tuple[list[PostCommentConfig], list[PostCommentConfig]] | None:
        if self.__follow_up is None:
            return None
        follow_up_1 = [PostCommentConfig(self._game, comment) for comment in self.__follow_up[0]]
        if self.same_follow_up:
            return follow_up_1, follow_up_1
        return follow_up_1, [PostCommentConfig(self._game, comment) for comment in self.__follow_up[1]]


class PostCommentConfig(View[filecfg.PostCommentConfig]):
    FileCfg: typing.Final = filecfg.PostCommentConfig

    @functools.cached_property
    def commentator(self) -> str:
        return self._game.text(self._filecfg.commentator)

    @functools.cached_property
    def text(self) -> str:
        return self._game.text(self._filecfg.text)
