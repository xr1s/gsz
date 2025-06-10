import typing

import pydantic
import typing_extensions

from . import aliases
from .base import ModelID

PARTNER_ICON = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "MMOAKKJMDKP",  # v2.0
        "CINKKNFJADK",  # v1.7
        "BIOLAILHJJJ",  # v1.6
        "GJGBNGDHGBI",  # v1.5
        "CLJPPGILNKD",  # v1.4
        "LGBKKDKEGFF",  # v1.3
        "MEOFLPHGDBO",  # v1.2
        "FFAIFNEIAGM",  # v1.1
    )
)
NAME = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "KGACNEEFAFN",  # v2.0
        "INNAIMOAPID",  # v1.7
        "EFPJLPJOBFL",  # v1.6
        "MEIDPJNKIDE",  # v1.5
        "BBAGGIAJFMD",  # v1.4
        "MDGBBLDPIPF",  # v1.3
        "LDPKGDEPFCH",  # v1.2
        "FAHEPAJDADB",  # v1.1
    )
)


class PartnerConfig(ModelID):
    partner_id: typing.Annotated[int, aliases.PARTNER_ID]
    avatar_id: typing.Annotated[int, aliases.AVATAR_ID]
    name: typing.Annotated[str, NAME]
    icon: typing.Annotated[str, PARTNER_ICON]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.partner_id
