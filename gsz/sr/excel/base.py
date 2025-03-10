import enum
import typing

import pydantic
import pydantic.alias_generators


class ID(typing.Protocol):
    def id(self) -> int: ...


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

    @typing.override
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


class Text(Model):
    hash: int


class Value[T](Model):
    value: T


ID_ALIASES = pydantic.AliasChoices(
    "KIFGIAMDGPI",  # 1.0
    "JEKCKJBHBKN",  # 1.1
    "MNMACAIHJCE",  # 1.2
    "CKFOCMJDLGG",  # 1.3
    "HMBDFGFHFAI",  # 1.4
    "OBBNCDOAKEF",  # 1.5
    "CMFIFDAHNOG",  # 1.6
    "DOHIPPHAGLG",  # 2.0
    "DGBJNJFOGHN",  # 2.1
    "ILOCKGFGCIF",  # 2.2
    "IPIGPCKIEMA",  # 2.3
    "IDNGFMLCGHB",  # 2.4
    "GKBBPHMLLNG",  # 2.5
    "PGKKLADJKGK",  # 2.6
    "CAMGCAFNKPK",  # 2.7
    "LDKCGGLDKCK",  # 3.0
    "BMEJEMLFEIO",  # 3.1
)

KEY_ALIASES = pydantic.AliasChoices(
    "JOAHDHLLMDK",  # 1.0
    "OEOPENFDEML",  # 1.1
    "LFCIILHABDO",  # 1.2
    "COJNNIIOEAK",  # 1.3
    "JDKAMOANICM",  # 1.4
    "CFNMGGCLFHN",  # 1.5
    "JJNBOIODCCF",  # 1.6
    "DJBGPLLGOEF",  # 2.0
    "CEDKLKIHFEK",  # 2.1
    "MLMLDHKBPLM",  # 2.2
    "LFKFFCJNFKN",  # 2.3
    "MBBNDDLBEPE",  # 2.4
    "PFMLCKGCKOB",  # 2.5
    "MFKLINKCPPA",  # 2.6
    "BNCHHJCHKON",  # 2.7
    "EGIHHBKIHAK",  # 3.0
    "HEIKKHLKMOA",  # 3.1
)

VAL_ALIASES = pydantic.AliasChoices(
    "LKJLPJMIGNJ",  # 1.0
    "BHLILFMLNEE",  # 1.1
    "LGKGOMNMBAH",  # 1.2
    "MBOHKHKHFPD",  # 1.3
    "MOJJBFBKBNC",  # 1.4
    "JCFBPDLNMLH",  # 1.5
    "AMMAAKPAKAA",  # 1.6
    "BOANKOCFAIM",  # 2.0
    "IEDALJJJBCE",  # 2.1
    "PKPGBCJMDEK",  # 2.2
    "EPBOOFFCKPJ",  # 2.3
    "DIBKEHHCPAP",  # 2.4
    "NLABNDMDIKM",  # 2.5
    "HPPEILAONGE",  # 2.6
    "ODPKJEJKOIH",  # 2.7
    "CPPHDJHHGGN",  # 3.0
    "MBMDOCJIMEJ",  # 3.1
)
