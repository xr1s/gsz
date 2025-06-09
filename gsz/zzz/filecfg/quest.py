import typing

import pydantic
import typing_extensions

from .base import ModelID

QUEST_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "PADEHJEHGLB",  # v2.0
        "JOCMKDOLBPP",  # v1.7
        "EKLGNOIEMLA",  # v1.6
        "GAKPNBMEMNG",  # v1.5
        "GCOCLELIFAG",  # v1.4
        "BEBBMAABIKA",  # v1.3
        "PGNNBMGHDEI",  # v1.2
        "PPPBBEOFKCC",  # v1.1
    )
)
QUEST_NAME = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "EKOEHAIFEHN",  # v2.0
        "CNLOKFIHOPC",  # v1.7
        "NIGGIDCENCK",  # v1.6
        "OOIJPMBPKOI",  # v1.5
        "DKEJAEFEJDL",  # v1.4
        "JLAJNFBMAJN",  # v1.3
        "LOHADDGODBE",  # v1.2
        "PEAELPCHHPG",  # v1.1
    )
)
QUEST_DESC = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
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
QUEST_TARGET = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "DLJGALBKDAN",  # v2.0
        "LFLPEENMECC",  # v1.7
        "HKLIDHMJIGB",  # v1.6
        "LGDDKFKADOA",  # v1.5
        "ABJIPBBKNOC",  # v1.4
        "POFFNMMOAIH",  # v1.3
        "IFBFAFDFKAP",  # v1.2
        "IPLPDPFPJGN",  # v1.1
    )
)
QUEST_FINISH_DEC = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "OCCMEAFDIIL",  # v2.0
        "KOGJLMNKEEH",  # v1.7
        "GIIEMDLFLGF",  # v1.6
        "HDPAMHDDFME",  # v1.5
        "CAKKDEIMFCM",  # v1.4
        "JGNFANJNOBE",  # v1.3
        "KNCIBCEHMII",  # v1.2
        "OJDIEIJKKML",  # v1.1
    )
)
QUEST_REWARD = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "DNCPKFPLPIF",  # v2.0
        "EAHEBGIBFMC",  # v1.7
        "LHIBKOLGPPI",  # v1.6
        "APOGDKCNLKK",  # v1.5
        "JCCGMOLGNNA",  # v1.4
        "NHPGJJBILJF",  # v1.3
        "MCBGAPHPMAO",  # v1.2
        "LPDGCALINGE",  # v1.1
    )
)


class QuestConfig(ModelID):
    quest_id: typing.Annotated[int, QUEST_ID]
    quest_name: typing.Annotated[str, QUEST_NAME]
    quest_desc: typing.Annotated[str, QUEST_NAME]
    quest_target: typing.Annotated[str, QUEST_TARGET]
    quest_finish_dec: typing.Annotated[str, QUEST_FINISH_DEC]
    reward: typing.Annotated[int, QUEST_REWARD]  # TODO: OnceRewardConfigTemplateTb.json

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.quest_id
