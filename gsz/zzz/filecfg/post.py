"""绳网"""

import typing

import pydantic
import typing_extensions

from . import aliases
from .base import ModelID

INTER_KNOT_ICON = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "MPAAKDHGIHE",  # v2.1
        "HJFJBBEKGHB",  # v2.0
        "LLPOAMPGPPF",  # v1.7
        "AFLMBEKEONA",  # v1.6
        "LGBGPFKHAIP",  # v1.5
        "KOCELOLDNFM",  # v1.4
        "PBBBPDEDOJP",  # v1.3
        "CODDKNDECBO",  # v1.2
        "KKHNBNGFCKE",  # v1.1
    )
)
INTER_KNOT_POSTER = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "BKLCKLBIPAH",  # v2.1
        "PKJGJPNPDGO",  # v2.0
        "PJFJKNAAGNF",  # v1.7
        "PCMCJPCOOBE",  # v1.6
        "MDGOCNKMBPN",  # v1.5
        "LKNEBLFJLKM",  # v1.4
        "MFCBKGINPFN",  # v1.3
        "NPCPKFKFNJH",  # v1.2
        "ELFJPBOABDN",  # v1.1
    )
)
INTER_KNOT_POST_TITLE = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "BIGDLKBBALP",  # v2.1
        "DEFAFCKGAPJ",  # v2.0
        "KKBHBNIELEC",  # v1.7
        "PGPOIMHKFPL",  # v1.6
        "CPPKKAJBAPF",  # v1.5
        "EICPJHCNGLM",  # v1.4
        "MDAOOOONAGO",  # v1.3
        "DOOMHDOCFPC",  # v1.2
        "PHLLPKKPDJA",  # v1.1
    )
)
INTER_KNOT_POST_TEXT = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "HKLJIIIPINE",  # v2.1
        "NMMLEAJABJL",  # v2.0
        "IHKFKNPKGNE",  # v1.7
        "CFDDOHAILFB",  # v1.6
        "MBBBAGJBGFJ",  # v1.5
        "BJCLJGJKAEA",  # v1.4
        "PGLCFCEJKPB",  # v1.3
        "JAEBMBAANNP",  # v1.2
        "EFCMDFEPABP",  # v1.1
    )
)
INTER_KNOT_POST_SCRIPT = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "KOICMLBIKOO",  # v2.1
        "HLMAALLJIAL",  # v2.0
        "OEAICGOGGEA",  # v1.7
        "DFFAAGNFLPN",  # v1.6
        "CJJJKBHINCH",  # v1.5
        "EBNJIIGOAMJ",  # v1.4
        "LKIGNEPPNLC",  # v1.3
        "GCCLBCPLLPL",  # v1.2
        "BIDMADGGDDP",  # v1.1
    )
)
INTER_KNOT_FOLLOW_UP_1 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "FJPJJNJIDGK",  # v2.1
        "IMPHIHCACEM",  # v2.0
        "ENKGNGGBMFA",  # v1.7
        "NEBGJHEHOED",  # v1.6
        "KMIDJGFGGOD",  # v1.5
        "HHFLMHJLJLB",  # v1.4
        "OFFLMOOPGNK",  # v1.3
        "HCFFBOCILDK",  # v1.2
        "DAFKKJEMBJK",  # v1.1
    )
)
INTER_KNOT_FOLLOW_UP_2 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "CKLDKBOCJBK",  # v2.1
        "JHKFKFFGCGM",  # v2.0
        "PDAKHHBCFIE",  # v1.7
        "MKAJGILECIP",  # v1.6
        "DEGPNDIDADB",  # v1.5
        "PPOBILCOOKC",  # v1.4
        "JCBDKMBCFMP",  # v1.3
        "IMLBNEDLFOL",  # v1.2
        "IAPOJENAKIF",  # v1.1
    )
)
# 不知道为什么 InterKnot 里用这个字段聚合
COMMENT_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "LBKDMFJENHL",  # v2.1
        "IKJJNJINMGC",  # v2.0
        "ECDKGGOGOGN",  # v1.7
        "KINEKLHNPOO",  # v1.6
        "KGPPOGANMGL",  # v1.5
        "HBJBMOANEOC",  # v1.4
        "HLMCFLOEGGO",  # v1.3
        "HHFJAJACEGD",  # v1.2
        "JEAHAKEBNNO",  # v1.1
    )
)


class InterKnotConfig(ModelID):
    id_: typing.Annotated[int, aliases.ID]
    icon: typing.Annotated[str, INTER_KNOT_ICON]
    poster: typing.Annotated[str, INTER_KNOT_POSTER]
    image: typing.Annotated[str, aliases.IMAGE]
    title: typing.Annotated[str, INTER_KNOT_POST_TITLE]
    text: typing.Annotated[str, INTER_KNOT_POST_TEXT]
    script: typing.Annotated[str, INTER_KNOT_POST_SCRIPT]
    reply_1: typing.Annotated[str, aliases.OPTION_1]
    """玩家评论选项"""
    follow_up_1: typing.Annotated[int, INTER_KNOT_FOLLOW_UP_1]
    """
    含义是玩家做完回复选择后弹出来的，跟在玩家回复之后的新回复
    """
    reply_2: typing.Annotated[str, aliases.OPTION_2]
    """玩家评论选项"""
    follow_up_2: typing.Annotated[int, INTER_KNOT_FOLLOW_UP_2]
    """
    含义是玩家做完回复选择后弹出来的，跟在玩家回复之后的新回复
    """
    comment_id: typing.Annotated[int, COMMENT_ID]
    """
    这里的 commentId 虽然和下面的 PostCommentConfig 主字段相同
    但实际上指的是 PostCommentConfig.groupId，是用于聚合评论的
    """

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


COMMENT_SORT = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "JIPKKLFNDNK",  # v2.1
        "DHECNJGJAFG",  # v2.0
        "IOINFILNFNF",  # v1.7
        "EBPFNIPBIFM",  # v1.6
        "MDOAOHOFJOF",  # v1.5
        "EDBCKMELGLO",  # v1.4
        "DIKOLFNDABO",  # v1.3
        "LEFNIPCJPOF",  # v1.2
        "IKOCMCDHIAF",  # v1.1
    )
)
COMMENT_ICON = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "AIHMONAHGHC",  # v2.1
        "PJPOOGMGPMF",  # v2.0
        "PFPBGJMJHBD",  # v1.7
        "LGBMNMGIIFK",  # v1.6
        "GNKCDIMNHGM",  # v1.5
        "PCHNMOKEGJJ",  # v1.4
        "HIDGNEEMNEJ",  # v1.3
        "PHCOHKGOMBJ",  # v1.2
        "CFHNKEHINEL",  # v1.1
    )
)
COMMENT_COMMENTATOR = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "INOIMGDCLMI",  # v2.1
        "OEIGHCGAMGC",  # v2.0
        "GBJAPHHCFHB",  # v1.7
        "JAGGFFNDJLP",  # v1.6
        "MHLPLANBNKB",  # v1.5
        "NJHOHNPJGCG",  # v1.4
        "OKIENKGJFHP",  # v1.3
        "GIDNDAIFHED",  # v1.2
        "DBDEACLHPGN",  # v1.1
    )
)
COMMENT_TEXT = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "BLMDAOKBNFP",  # v2.1
        "NFFDLNOFMCA",  # v2.0
        "JCMFPLKOJHG",  # v1.7
        "JNGJIMBEMCN",  # v1.6
        "PCLAFEKMNAE",  # v1.5
        "IOGEIDHNDLC",  # v1.4
        "FGKBHGPKOFO",  # v1.3
        "KPMCAILDAPP",  # v1.2
        "KIKNOLFDDFN",  # v1.1
    )
)


class PostCommentConfig(ModelID):
    comment_id: typing.Annotated[int, COMMENT_ID]
    group_id: typing.Annotated[int, aliases.GROUP_ID]
    """
    groupId 用于聚合同一个帖子下的不同回复，就是 InterKnot 的 commentId 字段（并非主字段）
    """
    sort: typing.Annotated[int, COMMENT_SORT]
    icon: typing.Annotated[str, COMMENT_ICON]
    commentator: typing.Annotated[str, COMMENT_COMMENTATOR]
    text: typing.Annotated[str, COMMENT_TEXT]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.comment_id
