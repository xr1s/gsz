import abc
import enum
import typing

import pydantic
import pydantic.alias_generators
import typing_extensions


class Element(enum.Enum):
    Fire = "Fire"
    """火"""
    Ice = "Ice"
    """冰"""
    Imaginary = "Imaginary"
    """虚数"""
    Physical = "Physical"
    """物理"""
    Quantum = "Quantum"
    """量子"""
    Thunder = "Thunder"
    """雷"""
    Wind = "Wind"
    """风"""

    @typing_extensions.override
    def __str__(self) -> str:  # noqa: PLR0911
        match self:
            case self.Fire:
                return "火"
            case self.Ice:
                return "冰"
            case self.Imaginary:
                return "虚数"
            case self.Physical:
                return "物理"
            case self.Quantum:
                return "量子"
            case self.Thunder:
                return "雷"
            case self.Wind:
                return "风"


ABBR_WORDS = {"ai", "bg", "hp", "id", "npc", "sp"}


def alias_generator(field_name: str) -> str:
    return "".join(word.upper() if word in ABBR_WORDS else word.capitalize() for word in field_name.split("_"))


class Model(pydantic.BaseModel):
    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        alias_generator=alias_generator,
        extra="forbid",
        frozen=True,
        populate_by_name=True,
    )


class ModelID(Model, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def id(self) -> int: ...


class ModelMainSubID(Model, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def main_id(self) -> int: ...

    @property
    @abc.abstractmethod
    def sub_id(self) -> int: ...


class Text(Model):
    hash: int


T = typing.TypeVar("T")


class Value(Model, typing.Generic[T]):
    value: T


FIELD_ALIASES_ID = pydantic.AliasChoices(
    "BMEJEMLFEIO",  # 3.1
    "LDKCGGLDKCK",  # 3.0
    "CAMGCAFNKPK",  # 2.7
    "PGKKLADJKGK",  # 2.6
    "GKBBPHMLLNG",  # 2.5
    "IDNGFMLCGHB",  # 2.4
    "IPIGPCKIEMA",  # 2.3
    "ILOCKGFGCIF",  # 2.2
    "DGBJNJFOGHN",  # 2.1
    "DOHIPPHAGLG",  # 2.0
    "CMFIFDAHNOG",  # 1.6
    "OBBNCDOAKEF",  # 1.5
    "HMBDFGFHFAI",  # 1.4
    "CKFOCMJDLGG",  # 1.3
    "MNMACAIHJCE",  # 1.2
    "JEKCKJBHBKN",  # 1.1
    "KIFGIAMDGPI",  # 1.0
)

FIELD_ALIASES_KEY = pydantic.AliasChoices(
    "HEIKKHLKMOA",  # 3.1
    "EGIHHBKIHAK",  # 3.0
    "BNCHHJCHKON",  # 2.7
    "MFKLINKCPPA",  # 2.6
    "PFMLCKGCKOB",  # 2.5
    "MBBNDDLBEPE",  # 2.4
    "LFKFFCJNFKN",  # 2.3
    "MLMLDHKBPLM",  # 2.2
    "CEDKLKIHFEK",  # 2.1
    "DJBGPLLGOEF",  # 2.0
    "JJNBOIODCCF",  # 1.6
    "CFNMGGCLFHN",  # 1.5
    "JDKAMOANICM",  # 1.4
    "COJNNIIOEAK",  # 1.3
    "LFCIILHABDO",  # 1.2
    "OEOPENFDEML",  # 1.1
    "JOAHDHLLMDK",  # 1.0
)

FIELD_ALIASES_ROGUE_WEEKLY_TYP = pydantic.AliasChoices(
    "PICHIHHCOCB",  # 3.1
    "PGCFPBGPDGG",  # 3.0
    "MPNJPFDCBDG",  # 2.7
    "EOMLKKGEAEF",  # 2.6
    "FGMDOEKGPEE",  # 2.5
    "EEOLCCFMJFF",  # 2.4
    "IAGLGKPDLOE",  # 2.3
)

FIELD_ALIASES_ROGUE_WEEKLY_VAL = pydantic.AliasChoices(
    "HMCDHMFHABF",  # 3.1
    "CPPHDJHHGGN",  # 3.0
    "ODPKJEJKOIH",  # 2.7
    "HPPEILAONGE",  # 2.6
    "NLABNDMDIKM",  # 2.5
    "DIBKEHHCPAP",  # 2.4
    "EPBOOFFCKPJ",  # 2.3
)

FIELD_ALIASES_VAL = pydantic.AliasChoices(
    "MBMDOCJIMEJ",  # 3.1
    "CPPHDJHHGGN",  # 3.0
    "ODPKJEJKOIH",  # 2.7
    "HPPEILAONGE",  # 2.6
    "NLABNDMDIKM",  # 2.5
    "DIBKEHHCPAP",  # 2.4
    "EPBOOFFCKPJ",  # 2.3
    "PKPGBCJMDEK",  # 2.2
    "IEDALJJJBCE",  # 2.1
    "BOANKOCFAIM",  # 2.0
    "AMMAAKPAKAA",  # 1.6
    "JCFBPDLNMLH",  # 1.5
    "MOJJBFBKBNC",  # 1.4
    "MBOHKHKHFPD",  # 1.3
    "LGKGOMNMBAH",  # 1.2
    "BHLILFMLNEE",  # 1.1
    "LKJLPJMIGNJ",  # 1.0
)
