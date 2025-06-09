import pydantic

"""
可以用以下方式获取旧版本的 Alias
但是不准确，因为可能有新加字段导致位置移动，需要手动观察一下

```bash
for v in v2.0 v1.{7..1}; do
  echo -n '"'
  git show ${v}:FileCfg/文件.json \
    | jq --join-output '.[] | keys[0]'
  echo "\",  # $v"
done
```
"""

EXP_FILE_CONFIG = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "LDABBJOAKGJ",  # v2.0
        "MCOOHPLIKCF",  # v1.7
        "GHFLHABGNDH",  # v1.6
        "HBEGBJCAGAJ",  # v1.5
        "LFPICNCBMIF",  # v1.4
        "PEPPKLMFFBD",  # v1.3
        "JIJNDLLPCHO",  # v1.2
        "KHHABHLHAFG",  # v1.1
    )
)

# AvatarBaseTemplateTb.json
ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "JCJHMPOONIA",  # v2.0
        "NHNBEFBOCMH",  # v1.7
        "OPFEAMDPIAG",  # v1.6
        "PDJOCPDOOAA",  # v1.5
        "FJKECLFEHOA",  # v1.4
        "GKNMDKNIMHP",  # v1.3
        "DKDDFEIAMIF",  # v1.2
        "NGPCCDGBLLK",  # v1.1
    )
)
# PartnerConfigTemplateTb.json
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

# 一般作为头像图标的字段名
# AvatarProfessionTemplateTb.json
ICON = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "HNLBNIBLAMJ",  # v2.0
        "BHHCFMLOCNO",  # v1.7
        "LEEEDDIMDGO",  # v1.6
        "FOPHNODPCIL",  # v1.5
        "HBJMCOAIBIC",  # v1.4
        "IJBKHFLGPHJ",  # v1.3
        "DBKGODAFDCP",  # v1.2
        "ELLAAEPEEPC",  # v1.1
    )
)

# 比如作为短信、绳网帖子z中图片字段名
# MessageGroupConfigTemplateTb.json
# InterKnotConfigTemplateTb.json
IMAGE = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "KOIJAKALEBB",  # v2.0
        "LMJJHCGEEKH",  # v1.7
        "BKDHNBKMLEH",  # v1.6
        "BCCFOCBBNHF",  # v1.5
        "DFFHKODPBOF",  # v1.4
        "KJOMPOAFJDP",  # v1.3
        "IEPLEDIIPIK",  # v1.2
        "ECICHGFPJKG",  # v1.1
    )
)

# MessageGroupConfigTemplateTb.json
GROUP_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "CDBNOFOLHHA",  # v2.0
        "JIODMKLIACL",  # v1.7
        "NJFOLJNDPGG",  # v1.6
        "HLLOEJMCGNH",  # v1.5
        "HPPLCCMACOO",  # v1.4
        "AKDKOOGEBIG",  # v1.3
        "HKMCIIBPBIL",  # v1.2
        "OLJJMDOAMMA",  # v1.1
    )
)

# PartnerConfigTemplateTb.json
AVATAR_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "MNFFGNFNAHF",  # v2.0
        "CLODPIMNGGD",  # v1.7
        "AMIJIAHGPMC",  # v1.6
        "HHOLJHONCGL",  # v1.5
        "FBEDJACHNDM",  # v1.4
        "FLDGKKJPIFL",  # v1.3
        "JAOENONJEBK",  # v1.2
        "JBHOICBGPLL",  # v1.1
    )
)

# PartnerConfigTemplateTb.json
PARTNER_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "CMKKLDCKGEP",  # v2.0
        "ALIBLMLOCPG",  # v1.7
        "IKDJDPPLNOM",  # v1.6
        "FPFBAONNLJE",  # v1.5
        "CPNCJFIDGJD",  # v1.4
        "MLKOGACEPJJ",  # v1.3
        "NOGICDBGMHG",  # v1.2
        "JOCCGJBAPNK",  # v1.1
    )
)

# MessageConfig PostCommentConfig
OPTION_1 = pydantic.Field(
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

# MessageConfigTemplateTb.json
# PostCommentConfigTemplateTb.json
OPTION_2 = pydantic.Field(
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
