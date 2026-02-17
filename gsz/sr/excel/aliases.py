import pydantic

# 3.2 ~ 3.7 的都和 3.1 一样没变过

# jq -Cc '.[].AISkillSequence[] | keys[]' MonsterTemplateConfig.json | sort -u
ID = pydantic.AliasChoices(
    "PMLIMKCDNJP",  # 4.0
    "JAJOONLKLBO",  # 3.8
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

# jq -Cc '.[].CustomValues[] | keys[]' MonsterConfig.json | sort -u
KEY = pydantic.AliasChoices(
    "MHHHCIPKDHL",  # 4.0
    "CHEAIJFINAB",  # 3.8
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

# jq -Cc '.[].CustomValues[] | keys[]' MonsterConfig.json | sort -u
VAL = pydantic.AliasChoices(
    "JOJNNKEPPLI",  # 4.0
    "GAGPCFOFKCN",  # 3.8
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

# jq -Cc '.[].DescParams[] | keys[]' RogueTournWeeklyDisplay.json | sort -u
ROGUE_WEEKLY_TYP = pydantic.AliasChoices(
    "ICMHAGLCJII",  # 4.0
    "EJAEDHBFJGI",  # 3.8
    "PICHIHHCOCB",  # 3.1
    "PGCFPBGPDGG",  # 3.0
    "MPNJPFDCBDG",  # 2.7
    "EOMLKKGEAEF",  # 2.6
    "FGMDOEKGPEE",  # 2.5
    "EEOLCCFMJFF",  # 2.4
    "IAGLGKPDLOE",  # 2.3
)

# jq -Cc '.[].DescParams[] | keys[]' RogueTournWeeklyDisplay.json | sort -u
ROGUE_WEEKLY_VAL = pydantic.AliasChoices(
    "IFIENLNPIJA",  # 4.0
    "CPALPNDAGBG",  # 3.8
    "HMCDHMFHABF",  # 3.1
    "CPPHDJHHGGN",  # 3.0
    "ODPKJEJKOIH",  # 2.7
    "HPPEILAONGE",  # 2.6
    "NLABNDMDIKM",  # 2.5
    "DIBKEHHCPAP",  # 2.4
    "EPBOOFFCKPJ",  # 2.3
)

# jq -Cc '.[] | keys[]' RogueBuffGroup.json | sort -u
ROGUE_BUFF_GROUP_ID = pydantic.AliasChoices(
    "IDLBMIHBAPB",  # 3.1
    "IKOLKLEFCGO",  # 3.0
    "BHOJPHAJLMI",  # 2.7
    "HFLJEIPCCNF",  # 2.6
    "IOMDAGGIAME",  # 2.5
    "MNNPAFJEGJC",  # 2.4
    "LIOICIOFLGL",  # 2.3
    "GKOGJPDANCE",  # 2.2
    "EGDAIIJDDPA",  # 2.1
    "GJHLAKLLFDI",  # 2.0
    "JHOKDPADHFM",  # 1.6
)

# jq -Cc '.[] | keys[]' RogueBuffGroup.json | sort -u
ROGUE_BUFF_DROP = pydantic.AliasChoices(
    "GNGDPDOMDFH",  # 3.1
    "DKLEHCPFLFJ",  # 3.0
    "NDFFCMBIOAG",  # 2.7
    "ILLJGPJPFAC",  # 2.6
    "HLKMFHBOAIA",  # 2.5
    "KCFPNHGBGIA",  # 2.4
    "LEEMGFGKCMO",  # 2.3
    "NFPAICKGMBC",  # 2.2
    "AMGHNOBDGLM",  # 2.1
    "DNKFBOAIDCE",  # 2.0
    "ADJICNNJFEM",  # 1.6
)

# jq -Cc '.[].UnlockNPCProgressIDList[] | keys[]' RogueHandBookEvent.json | sort -u
UNLOCK_NPC_ID = pydantic.AliasChoices(
    "HHGAFBNILGL",  # 3.8
    "MBNKLBEBOHB",  # 3.1
    "HLNMOFDGLAA",  # 3.0
    "KOPDNGGIFKN",  # 2.7
    "GNBAICOJALE",  # 2.6
    "GFKCKEKCGIB",  # 2.5
    "FBIOIFGPFHI",  # 2.4
    "AFFNNEIMKBG",  # 2.3
)

# jq -Cc '.[].UnlockNPCProgressIDList[] | keys[]' RogueHandBookEvent.json | sort -u
UNLOCK_PROGRESS = pydantic.AliasChoices(
    "ANLHDPFLCBM",  # 3.1
    "NNDEOKKKKPE",  # 3.1
    "AFMKGEHANLM",  # 3.0
    "FINLPBFNLHP",  # 2.7
    "EJJEHNGJCJH",  # 2.6
    "EEMMLHDLGKP",  # 2.5
    "HMGKHONMICH",  # 2.4
    "IMFEHFHGNNI",  # 2.3
)

# jq -Cc '.[].SubLevelGraphs[] | keys[]' StageConfig.json | sort -u
STAGE_SUBLEVELGRAPH_UNKNOW_0 = pydantic.AliasChoices("AIOKHBKLIFC", "JKJIKCPOENJ", "KDPPOPPKFAM")
STAGE_SUBLEVELGRAPH_UNKNOW_1 = pydantic.AliasChoices("COLFEFDGFLG", "EDGBKLAOIKD", "PEMNGOFOKLJ")
STAGE_SUBLEVELGRAPH_UNKOWN_2 = pydantic.AliasChoices("LADCKGAMEEN", "JCLEKCFPDJK", "DMNAIOFLJNC")
STAGE_SUBLEVELGRAPH_UNKOWN_3 = pydantic.AliasChoices("ALCCFKDDOIE", "MNKCMBDMGNB")
STAGE_SUBLEVELGRAPH_UNKOWN_4 = pydantic.AliasChoices("MMHHFHAFJPP", "MDIPBLCKGIG")
STAGE_SUBLEVELGRAPH_UNKOWN_5 = pydantic.AliasChoices("JLKMCEEILEP", "HFIFCMOGPFC")
