import typing

import pydantic
import typing_extensions

from .base import ModelID

ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "DPGJBGIBMJH",  # v2.1
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
NAME = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "ANFFBODIJJN",  # v2.1
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
DESC = pydantic.Field(
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
TARGET = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "HDEMCCKJGBM",  # v2.1
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
FINISH_DEC = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "CBMGOMFCDIM",  # v2.1
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
REWARD = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "HBJEOFPHPKB",  # v2.1
        "DNCPKFPLPIF",  # v2.0
        "EAHEBGIBFMC",  # v1.7
        "LHIBKOLGPPI",  # v1.6
        "APOGDKCNLKK",  # v1.5
        "JCCGMOLGNNA",  # v1.4
        "NHPGJJBILJF",  # v1.3
        "LIAHOJOIDMJ",  # v1.2
        "PCBMFGJCLDA",  # v1.1
    )
)


class QuestConfig(ModelID):
    id_: typing.Annotated[int, ID]
    name: typing.Annotated[str, NAME]
    desc: typing.Annotated[str, DESC]
    target: typing.Annotated[str, TARGET]
    finish_dec: typing.Annotated[str, FINISH_DEC]
    reward: typing.Annotated[int, REWARD]  # TODO: OnceRewardConfigTemplateTb.json

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
