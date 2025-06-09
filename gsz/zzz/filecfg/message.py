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
MESSAGE_OPTION_01 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "ANOGLHNNINL",  # v2.0
        "DPMNGFBMPAI",  # v1.7
        "EKENONMBDFB",  # v1.6
        "EAOGJNHGNCC",  # v1.5
        "BGBBDHKHABJ",  # v1.4
        "AFFFAGHMCKI",  # v1.3
        "JCCNCNCPGNM",  # v1.2
        "GMFFDAKPFNL",  # v1.1
    )
)
MESSAGE_OPTION_LONG_01 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
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
MESSAGE_OPTION_02 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "IJDJPMIHHEH",  # v2.0
        "GPJNDHPMKIN",  # v1.7
        "MIJDGAIGNCA",  # v1.6
        "EKMIILMACOD",  # v1.5
        "FOKHEIPDGDM",  # v1.4
        "EHPPNFEALOE",  # v1.3
        "CEDEPEBICEL",  # v1.2
        "GOMFGFAGNFB",  # v1.1
    )
)
MESSAGE_OPTION_LONG_02 = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
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
        # "PFHPPCKEHCO",  # v2.0
        # "OPDCEDDFFAG",  # v1.7
        # "CFIJJNBPFPP",  # v1.6
        # "EHPIOMJJJHI",  # v1.5
        # "EPJLJOIDBHI",  # v1.4
        # "JIKICBFNCDP",  # v1.3
        # "ADEMJOAEJOL",  # v1.2
        # "EMFBKODOKLE",  # v1.1
        "FJIGNDBDFGH",  # v2.0
        "JLBFBBIBKFN",  # v1.7
        "MBEKPIEKHBO",  # v1.6
        "MEDLNFDMBKE",  # v1.5
        "IFNFKFHHOMD",  # v1.4
        "ONIFFJGGOOI",  # v1.3
        "LKFOPNJCJBA",  # v1.2
        "FMMIBDPEOHB",  # v1.1
    )
)


class MessageConfig(ModelID):
    id_: typing.Annotated[int, aliases.ID]
    group_id: typing.Annotated[int, aliases.GROUP_ID]
    sender_id: typing.Annotated[int, MESSAGE_SENDER_ID]
    text: typing.Annotated[str, MESSAGE_TEXT]
    option_01: typing.Annotated[str, MESSAGE_OPTION_01]
    option_long_01: typing.Annotated[str, MESSAGE_OPTION_LONG_01]
    option_02: typing.Annotated[str, MESSAGE_OPTION_02]
    option_long_02: typing.Annotated[str, MESSAGE_OPTION_LONG_02]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


MESSAGE_GROUP_CONTACT_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
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


class MessageGroupConfig(ModelID):
    group_id: typing.Annotated[int, aliases.GROUP_ID]
    contact_id: typing.Annotated[int, MESSAGE_GROUP_CONTACT_ID]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.group_id


MESSAGE_NPC_NAME = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
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
