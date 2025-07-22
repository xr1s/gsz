import enum
import typing

import pydantic
import typing_extensions

from . import aliases
from .base import ModelID

DIRECTORY_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "HOIBJBLPOFG",  # v2.0
        "EGEPBDDPMNF",  # v1.7
        "KGIOLPOGHMP",  # v1.6
        "BFDJHEAIECI",  # v1.5
        "HFBOIKNHOLH",  # v1.4
        "NOMADJDAIME",  # v1.3
        "KEIIIGFBNGE",  # v1.2
        "AFNOOJLPBNH",  # v1.1
    )
)
DIRECTORY_IMPRESSION_1 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "AFGALHGAMMI",  # v2.0
        "FGHFKGBLILD",  # v1.7
        "KACKPENIGJE",  # v1.6
        "LOMGIPCPJKE",  # v1.5
        "NHNPKENMHID",  # v1.4
        "LGKBAPOHFMA",  # v1.3
        "HKIGCALNLDE",  # v1.2
        "IKKKLNALIMH",  # v1.1
    )
)
DIRECTORY_IMPRESSION_2 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "JEFDGPADAGF",  # v2.0
        "PIKOMIKFDBH",  # v1.7
        "BOAMHAGIOLI",  # v1.6
        "JMMLIGPEGFK",  # v1.5
        "DAEJCAILLFA",  # v1.4
        "PFPEAKLBFLG",  # v1.3
        "JCIHFHOPJOC",  # v1.2
        "JFPIFDHIDPN",  # v1.1
    )
)
DIRECTORY_IMPRESSION_3 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "AOBOAEAKMDJ",  # v2.0
        "LBLMKNNDFJM",  # v1.7
        "NMFDMONLFFL",  # v1.6
        "KDPMMELHKIO",  # v1.5
        "HDHFHPAFIOB",  # v1.4
        "POBPBNKFDAP",  # v1.3
        "FLPNJHGLNCJ",  # v1.2
        "PHNMKLOJEDL",  # v1.1
    )
)


class DirectoryConfig(ModelID):
    partner_id: typing.Annotated[int, aliases.PARTNER_ID]
    directory_id: typing.Annotated[int, DIRECTORY_ID]
    impression_1: typing.Annotated[str, DIRECTORY_IMPRESSION_1]
    impression_2: typing.Annotated[str, DIRECTORY_IMPRESSION_2]
    impression_3: typing.Annotated[str, DIRECTORY_IMPRESSION_3]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.directory_id


MESSAGE_TEXT = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "DECDHOMFHKM",  # v2.1
        "CGEBBEENHED",  # v2.0
        "LKJJLBFHPHD",  # v1.1
        "OODFKPPKAAG",  # v1.2
        "ADLLEFKPOEP",  # v1.3
        "EKGNLANNFLB",  # v1.4
        "NMPCJGHNAIN",  # v1.5
        "NMMADBDFJCK",  # v1.6
        "KAJBKJKMHOM",  # v1.7
    )
)
MESSAGE_OPTION_LONG_1 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "ODCPPAKEEPM",  # v2.1
        "MDGHOIDHADH",  # v2.0
        "HCMBGLFKOLH",  # v1.7
        "JNPFKHLFHJM",  # v1.6
        "AJLMJCEINKE",  # v1.5
        "FNMDEBIGBDE",  # v1.4
        "CPMMFIHMEDE",  # v1.3
        "FKINNMOBOCP",  # v1.2
        "CENCINKPEKA",  # v1.1
    )
)
MESSAGE_OPTION_LONG_2 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "NGADKHLFKDI",  # v2.1
        "DNNDOHCBDHO",  # v2.0
        "FIIFOCIBPFB",  # v1.7
        "KGAOABEJECO",  # v1.6
        "JLJHLJANCCH",  # v1.5
        "EFANBOHMKAH",  # v1.4
        "ANLDLGIONOC",  # v1.3
        "FONPLGJOBMK",  # v1.2
        "PAJGHHKFEBC",  # v1.1
    )
)
MESSAGE_SENDER_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "POAKMNJMIAJ",  # v2.1
        "PFHPPCKEHCO",  # v2.0
        "OPDCEDDFFAG",  # v1.7
        "CFIJJNBPFPP",  # v1.6
        "EHPIOMJJJHI",  # v1.5
        "EPJLJOIDBHI",  # v1.4
        "JIKICBFNCDP",  # v1.3
        "ADEMJOAEJOL",  # v1.2
        "EMFBKODOKLE",  # v1.1
        # 下面的是另一个字段，有些时候是 0，但好像也不是发信人
        # "FJIGNDBDFGH",  # v2.0
        # "JLBFBBIBKFN",  # v1.7
        # "MBEKPIEKHBO",  # v1.6
        # "MEDLNFDMBKE",  # v1.5
        # "IFNFKFHHOMD",  # v1.4
        # "ONIFFJGGOOI",  # v1.3
        # "LKFOPNJCJBA",  # v1.2
        # "FMMIBDPEOHB",  # v1.1
    )
)
MESSAGE_VOICE = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "ABAJINNBCEA",  # v2.1
        "NMAEHDCKFEL",  # v2.0
        "LANAEOPKBLO",  # v1.7
        "JCLHDCHMOFH",  # v1.6
        "BIHFFLMDHIL",  # v1.5
        "JKBLKDOKGNM",  # v1.4
        "MDJINNLAJJO",  # v1.3
        "GOBMMPBNOGE",  # v1.2
        "OGBAPJEEBLH",  # v1.1
        # 下面的是另一个字段，但是值完全相同
        # "DCAPBBIKKDL",  # v2.0
        # "DFDAJIMKHAP",  # v1.7
        # "AFJCFEBLLPP",  # v1.6
        # "PIKOJIKHEBF",  # v1.5
        # "NJFEGLOMCMD",  # v1.4
        # "ECBBLGANCKP",  # v1.3
        # "HPDAHKEKLKI",  # v1.2
        # "JAFGOFDBJIP",  # v1.1
    )
)
MESSAGE_SEGMENT = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "BKOAPELPEGL",  # v2.1
        "ILLNMKIDBOC",  # v2.0
        "OPCPFJMMICA",  # v1.7
        "MIMIKGPBOFG",  # v1.6
        "JMNNPIGLDMA",  # v1.5
        "JHNKDJMCFBA",  # v1.4
        "IGCCHBECFCN",  # v1.3
        "CLICHHGFGLJ",  # v1.2
        "CDHCJFKGIAL",  # v1.1
    )
)
MESSAGE_TYPE = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "AAJNLGHFKID",  # v2.1
        "DCLLHMMFDOG",  # v2.0
        "PPKFFBLPHDK",  # v1.7
        "HPNGGPKBBJG",  # v1.6
        "GNDFAMKDBAA",  # v1.5
        "FBJOIIJKOKP",  # v1.4
        "NAPLJAKKKME",  # v1.3
        "HPEEJOCGJGE",  # v1.2
        "IDNHILJCENI",  # v1.1
    )
)
MESSAGE_SUCCESSOR = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "AFNINBBDCOF",  # v2.1
        "FIAJBANCPMD",  # v2.0
        "MBPHJOGEKKA",  # v1.7
        "FDLBBFNBCNP",  # v1.6
        "GIKJGLJJOFP",  # v1.5
        "IJJOABHABFO",  # v1.4
        "IBANEAGGFBO",  # v1.3
        "OFLBECMHKNM",  # v1.2
        "ODMLGIECNEE",  # v1.1
    )
)
MESSAGE_OPTION_SUCCESSOR_1 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "PFEFHIBHJDL",  # v2.1
        "DMPOBPACNFG",  # v2.0
        "ABGCJDOAKHN",  # v1.7
        "GFCBLLMBFEH",  # v1.6
        "HMLBEODKNID",  # v1.5
        "NNHNKGHIDAE",  # v1.4
        "AELKAMJKGBI",  # v1.3
        "CHHEADLAHID",  # v1.2
        "ABOHGBNOHMA",  # v1.1
    )
)
MESSAGE_OPTION_SUCCESSOR_2 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "KBIFFIEJJMO",  # v2.1
        "CBFAFJMBLDO",  # v2.0
        "HKIPEMBOLEC",  # v1.7
        "AHPEAHJMJGC",  # v1.6
        "JECCOJCGKFO",  # v1.5
        "GJNBLIAIEML",  # v1.4
        "KHIMOEDNBHC",  # v1.3
        "DEAGPHNNPGL",  # v1.2
        "GLBCCGJMHFM",  # v1.1
    )
)


class Type(enum.Enum):
    Text = 0
    """正文，此时只有 text 非空"""
    Option = 1
    """选项"""
    ImageOption = 2
    """图片选项"""
    Mission = 3
    """接取任务按钮，游戏中具体表现形式和任务类型有关"""


class MessageConfig(ModelID):
    group_id: typing.Annotated[int, aliases.GROUP_ID]
    id_: typing.Annotated[int, aliases.ID]
    sender_id: typing.Annotated[int, MESSAGE_SENDER_ID]
    voice: typing.Annotated[str, MESSAGE_VOICE]
    text: typing.Annotated[str, MESSAGE_TEXT]
    image: typing.Annotated[str, aliases.IMAGE]
    """图片或表情 Emoji"""
    segment: typing.Annotated[int, MESSAGE_SEGMENT]
    """
    用来实现短信选项分支的字段
    segment 是一个同 group_id 不重复的编号，表示这一条消息属于哪个分段
    在每个 option 之后会出现一个字段，表示选择该选项后继进入哪个分段
    """
    type: typing.Annotated[Type, MESSAGE_TYPE]
    successor: typing.Annotated[int, MESSAGE_SUCCESSOR]
    """
    表示这条消息结束后跳转到哪个 segment，仅针对非选项消息
    """
    option_1: typing.Annotated[str, aliases.OPTION_1]
    """第一个选项文案"""
    option_long_1: typing.Annotated[str, MESSAGE_OPTION_LONG_1]
    """表示选择第一个选项后玩家实际发送的文字"""
    option_successor_1: typing.Annotated[int, MESSAGE_OPTION_SUCCESSOR_1]
    """表示选择第一个选项后，后续进入哪个 segment 对应的分支"""
    option_2: typing.Annotated[str, aliases.OPTION_2]
    """第二个选项文案"""
    option_long_2: typing.Annotated[str, MESSAGE_OPTION_LONG_2]
    """表示选择第二个选项后玩家实际发送的文字"""
    option_successor_2: typing.Annotated[int, MESSAGE_OPTION_SUCCESSOR_2]
    """表示选择第二个选项后，后续进入哪个 segment 对应的分支"""

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


MESSAGE_GROUP_CONTACT_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "JJFNJOLFJMD",  # v2.1
        "BOKBNFBPHHM",  # v2.0
        "MECCALDLPJB",  # v1.7
        "HBHCMOIIIKN",  # v1.6
        "GAPCAIHGNHK",  # v1.5
        "NHFICJDBHNE",  # v1.4
        "AIIDMBEFNMF",  # v1.3
        "MGMKCKHBKKL",  # v1.2
        "JMDGJCBENMP",  # v1.1
    )
)
MESSAGE_GROUP_QUEST_IDS = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "LOFIBCAAGBD",  # v2.1
        "DCAPBBIKKDL",  # v2.0
        "DFDAJIMKHAP",  # v1.7
        "AFJCFEBLLPP",  # v1.6
        "PIKOJIKHEBF",  # v1.5
        "NJFEGLOMCMD",  # v1.4
        "ECBBLGANCKP",  # v1.3
        "HPDAHKEKLKI",  # v1.2
        "JAFGOFDBJIP",  # v1.1
    )
)


class MessageGroupConfig(ModelID):
    group_id: typing.Annotated[int, aliases.GROUP_ID]
    contact_id: typing.Annotated[int, MESSAGE_GROUP_CONTACT_ID]
    quest_ids: typing.Annotated[list[int], MESSAGE_GROUP_QUEST_IDS]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.group_id


MESSAGE_NPC_NAME = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "LNCODBGHFKM",  # v2.1
        "LMFGBBIIMNL",  # v2.0
        "MLGCKOOKMHN",  # v1.7
        "MPHLIEKKFIK",  # v1.6
        "KMFMLNCJBEG",  # v1.5
        "JOMJELIIAGO",  # v1.4
        "FJECNNMMDGH",  # v1.3
        "DEPJKIPACJK",  # v1.2
        "EAAFCGPDFAA",  # v1.1
    )
)


class MessageNPC(ModelID):
    id_: typing.Annotated[int, aliases.ID]
    icon: typing.Annotated[str, aliases.ICON]
    name: typing.Annotated[str, MESSAGE_NPC_NAME]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
