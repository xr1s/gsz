import datetime
import typing

import pydantic

from .base import GameId, Model
from .image import Image
from .structured_content import StructuredContent, validate_twice
from .vod import Vod


class PostStatus(Model):
    is_top: bool
    is_good: bool
    is_official: bool
    post_status: typing.Literal[0]


class MetaContent(Model):
    class Vod(Model):
        id: int

    describe: list[StructuredContent]
    vods: list[Vod] | None = None
    activity_meta: typing.Annotated[None, pydantic.Field(alias="ActivityMeta")] = None

    @staticmethod
    def validate_twice(value: bytes) -> "MetaContent | None":
        if len(value) == 0:
            return None
        return MetaContent.model_validate_json(value)


class Post(Model):
    game_id: GameId
    post_id: int
    f_forum_id: int
    uid: int
    subject: str
    content: str
    cover: typing.Literal[""] | pydantic.HttpUrl
    view_type: typing.Literal[1, 2, 4, 5]
    created_at: datetime.datetime
    images: list[pydantic.HttpUrl]
    post_status: PostStatus
    topic_ids: list[int]
    view_status: typing.Literal[1]
    max_floor: int
    is_original: typing.Literal[0, 1, 2]
    republish_authorization: typing.Literal[0, 2]
    reply_time: datetime.datetime
    is_deleted: typing.Literal[0]
    is_interactive: typing.Literal[0]
    structured_content: typing.Annotated[list[StructuredContent] | None, pydantic.BeforeValidator(validate_twice)]
    structured_content_rows: list[None]
    review_id: int
    is_profit: bool
    is_in_profit: bool
    summary: str
    is_missing: bool
    pre_pub_status: typing.Literal[0]
    profit_post_status: typing.Literal[-2]
    is_showing_missing: bool
    block_reply_img: int
    is_mentor: bool
    updated_at: datetime.datetime
    deleted_at: typing.Literal[0] | datetime.datetime
    cate_id: int
    audit_status: typing.Literal[0]
    meta_content: typing.Annotated[MetaContent | None, pydantic.BeforeValidator(MetaContent.validate_twice)]
    block_latest_reply_time: typing.Literal[0]
    selected_comment: int


class ForumCate(Model):
    id: int
    name: str
    forum_id: int


class Forum(Model):
    id: int
    name: str
    icon: pydantic.HttpUrl
    game_id: GameId
    forum_cate: ForumCate | None = None


class Topic(Model):
    id: int
    name: str
    cover: pydantic.HttpUrl
    is_top: bool
    is_good: bool
    is_interactive: bool
    game_id: typing.Literal[0] | GameId
    content_type: typing.Literal[1, 2, 3]


class Certification(Model):
    type: typing.Literal[1]
    label: str


class LevelExp(Model):
    level: int
    exp: int


class AvatarExt(Model):
    avatar_type: typing.Literal[0]
    avatar_assets_id: typing.Literal[""]
    resources: list[None]
    hd_resources: list[None]


class PostUpvoteStat(Model):
    upvote_type: typing.Literal[1, 2, 3, 4, 5]
    """点赞表情类型"""
    upvote_cnt: int


class Stat(Model):
    view_num: int
    reply_num: int
    like_num: int
    bookmark_num: int
    forward_num: int
    post_upvote_stat: list[PostUpvoteStat]
    original_like_num: int


class SelfOperation(Model):
    attitude: typing.Literal[0]
    is_collected: bool
    upvote_type: typing.Literal[0]


class User(Model):
    uid: int
    nickname: str
    introduce: str
    avatar: typing.Literal[""] | int
    gender: typing.Literal[0]
    certification: Certification
    level_exp: LevelExp
    is_following: bool
    is_followed: bool
    avatar_url: pydantic.HttpUrl
    pendant: typing.Literal[""] | pydantic.HttpUrl
    """头像装饰"""
    certifications: list[Certification]
    is_creator: bool
    avatar_ext: AvatarExt


class UserPost(Model):
    post: Post
    forum: Forum | None
    topics: list[Topic]
    user: User
    self_operation: SelfOperation
    stat: Stat
    cover: Image | None = None
    image_list: list[Image]
    is_official_master: bool
    is_user_master: bool
    hot_reply_exist: bool
    vote_count: int
    last_modify_time: typing.Literal[0] | datetime.datetime
    recommend_type: typing.Literal[""]
    collection: None
    vod_list: list[Vod]
    is_block_on: bool
    forum_rank_info: None
    link_card_list: list[None]
    news_meta: None
    recommend_reason: None
    villa_card: None
    is_mentor: bool
    villa_room_card: None
    reply_avatar_action_info: None
    challenge: None
    hot_reply_list: list[None]
    villa_msg_image_list: list[None]
    is_has_vote: bool
    is_has_lottery: bool
    text_summary: typing.Literal[""]
    brief_structured_content: typing.Literal[""]


class UserPostList(Model):
    list: list[UserPost]
    is_last: bool
    next_offset: int
