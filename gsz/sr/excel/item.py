import enum
import typing

import pydantic

from .base import Model, Text


class MainType(enum.Enum):
    AvatarCard = "AvatarCard"
    """角色，仅出现在 ItemConfigAvatar.json 和 ActivityItemConfigAvatar.json 中"""
    Display = "Display"
    """
    有个图标用来展示，实际不存在的道具
    出现在黑塔模拟宇宙遗器模板
    """
    Equipment = "Equipment"
    """光锥，仅出现在 ItemConfigEquipment.json 中"""
    Material = "Material"
    """各种材料，非常多非常杂，参见 ItemSubType"""
    Mission = "Mission"
    """任务道具"""
    Pet = "Pet"
    """随宠"""
    Relic = "Relic"
    """遗器，仅出现在 ItemConfigRelic.json 中"""
    Usable = "Usable"
    """可交互的（可消耗、可阅读）"""
    Virtual = "Virtual"
    """
    各种不占据背包格子的数值项
    比如星琼、信用点、经验、开拓力、各类活动金币等
    """


class SubType(enum.Enum):
    AetherSkill = "AetherSkill"
    """
    以太战线技能芯片
    对应 ItemMainType 为 Material
    """
    AetherSpirit = "AetherSpirit"
    """
    以太战线宠物
    对应 ItemMainType 为 Material
    """
    AvatarCard = "AvatarCard"
    """
    角色
    仅出现在 ItemConfigAvatar.json 和 ActivityItemConfigAvatar.json 中
    对应 ItemMainType 为 AvatarCard
    """
    AvatarSkin = "AvatarSkin"
    """
    角色皮肤
    仅出现在 ItemConfigAvatarSkin.json 中
    """
    Book = "Book"
    """
    书籍
    对应 ItemMainType 为 Usable
    对应 UseMethod 为 AutoConversionItem 自动转换
    """
    ChatBubble = "ChatBubble"
    """
    对话框
    对应 ItemMainType 为 Usable
    对应 UseMethod 为 AutoConversionItem 自动转换
    """
    ChessRogueDiceSurface = "ChessRogueDiceSurface"
    """
    黄金与机械骰面
    对应 ItemMainType 为 Usable
    对应 UseMethod 为 AutoConversionItem 自动转换
    """
    Eidolon = "Eidolon"
    """星魂, 仅出现在 ItemConfigAvatarRank.json 中"""
    Equipment = "Equipment"
    """光锥, 仅出现在 ItemConfigEquipment.json 中"""
    FightFestSkill = "FightFestSkill"
    """
    星天演武仪典技能和饮料
    对应 ItemMainType 为 Material
    """
    FindChest = "FindChest"
    """3.0 新增寻宝道具"""
    Food = "Food"
    """
    食品
    对应 ItemMainType 为 Usable
    """
    ForceOpitonalGift = "ForceOpitonalGift"
    """
    一般是游戏赠送光锥、角色时使用的道具
    对应 ItemMainType 为 Usable
    """
    Formula = "Formula"
    """
    合成配方
    对应 ItemMainType 为 Usable
    """
    GameplayCounter = "GameplayCounter"
    """
    怪物隐身玩法
    资源废弃，只在 1.6 及之前出现
    """
    Gift = "Gift"
    """
    各种兑换类道具（包括商城礼包）
    对应 ItemMainType 为 Usable
    对应 UseMethod 为：
    大小月卡四种 MonthlyCard, BPUnlock68, BPUnlock128, BPUpgradeFrom68To128
    固定奖励 FixedRewardGift, 随机奖励 RandomRewardGift, 用户选择奖励 PlayerSelectedReward
    """
    HeadIcon = "HeadIcon"
    """用户头像"""
    Material = "Material"
    """
    非常杂, ItemMainType 为 Material 的剩下的都在里面
    包括但不限于角色, 天赋, 武器的突破材料, 周本材料; 遗器, 角色, 武器经验等
    抽卡用的专票、通票等，各种活动积分等
    """
    Mission = "Mission"
    """任务道具, ItemMainType 为 Mission 的都在这里"""
    MuseumExhibit = "MuseumExhibit"
    """
    冬城博物馆活动的展览品
    对应 ItemMainType 为 Material
    """
    MuseumStuff = "MuseumStuff"
    """
    冬城博物馆活动的员工
    对应 ItemMainType 为 Material
    """
    MusicAlbum = "MusicAlbum"
    """碟片（音乐专辑）"""
    NormalPet = "NormalPet"
    """
    随宠
    对应 ItemMainType 为 Pet
    """
    PamSkin = "PamSkin"
    """
    帕姆皮肤，派对车厢皮肤
    对应的 ItemMainType 为 Usable
    """
    PhoneTheme = "PhoneTheme"
    """
    手机主题
    对应 ItemMainType 为 Usable
    对应 UseMethod 为 AutoConversionItem 自动转换
    """
    Relic = "Relic"
    """遗器"""
    RelicRarityShowOnly = "RelicRarityShowOnly"
    """
    图标展示用, 位面饰品套装图，代表任意的位面饰品
    出现在黑塔空间站地图上黑塔办公室传送点的沉浸奖励一栏
    对应 ItemMainType 为 Display
    """
    RelicSetShowOnly = "RelicSetShowOnly"
    """
    图标展示用, 位面饰品套装图，不是绳球分别的遗器
    出现在模拟宇宙主界面提示每个宇宙能获得哪种套装的沉浸奖励处
    对应 ItemMainType 为 Display
    """
    RogueMedal = "RogueMedal"
    """差分宇宙概率艺术馆展品"""
    TrainPartyDiyMaterial = "TrainPartyDiyMaterial"
    """开拓者房间装饰品（宇宙家装指南活动）"""
    TravelBrochurePaster = "TravelBrochurePaster"
    """
    匹诺康尼梦境护照上的贴纸
    对应 ItemMainType 是 Usable
    """
    Virtual = "Virtual"
    """
    各种不占据背包格子的数值项
    比如星琼、信用点、经验、开拓力、各类活动金币等
    """


class Rarity(enum.Enum):
    Normal = "Normal"
    """一星"""
    NotNormal = "NotNormal"
    """二星"""
    Rare = "Rare"
    """三星"""
    VeryRare = "VeryRare"
    """四星"""
    SuperRare = "SuperRare"
    """五星"""

    @typing.override
    def __str__(self) -> str:
        match self:
            case self.Normal:
                return "一星"
            case self.NotNormal:
                return "二星"
            case self.Rare:
                return "三星"
            case self.VeryRare:
                return "四星"
            case self.SuperRare:
                return "五星"


class UseMethod(enum.Enum):
    AutoConversionItem = "AutoConversionItem"
    """自动转换为图鉴等道具. 目前有图书, 聊天框, 黄金与机械骰面, 手机主题四种."""
    BPUnlock128 = "BPUnlock128"
    """128 月卡"""
    BPUnlock68 = "BPUnlock68"
    """68 月卡"""
    BPUpgradeFrom68To128 = "BPUpgradeFrom68To128"
    """68 月卡升级 128 月卡道具"""
    ExternalSystemFoodBenefit = "ExternalSystemFoodBenefit"
    """
    食物效果, 往往是战斗增益或减益.
    当 UseMethod 为此时, 会通过 UseDataID 关联到 ItemUseData.json
    再通过对应 ItemUseData 对象的 UerParam 作为主键关联到 ItemBuffData.json
    具体数值通过 ItemBuffData 的 MazeBuffID 关联到 MazeBuff.json
    """
    FightFestMemorialPaper = "FightFestMemorialPaper"
    """只有一个星天演武仪典的纪念道具"""
    FindChest = "FindChest"
    """3.0 新增寻宝罗盘"""
    FixedRewardGift = "FixedRewardGift"
    """
    固定奖励
    当 UseMethod 为此时, 会通过 UseDataID 关联到 ItemUseData.json
    再通过对应 ItemUseData 对象的 UerParam 作为主键关联到 RewardData.json
    再通过 RewardData 的 ItemID_* 作为主键关联到角色、光锥或道具
    """
    MonthlyCard = "MonthlyCard"
    """30 月卡"""
    PetSummonRecall = "PetSummonRecall"
    """随宠"""
    PlayerSelectedReward = "PlayerSelectedReward"
    """
    用户多选一, 一般是活动的角色或者光锥奖励
    当 UseMethod 为此时, 会通过 UseDataID 关联到 ItemUseData.json
    再通过对应 ItemUseData 对象的 UerParam 作为主键关联到 RewardData.json
    再通过 RewardData 的 ItemID_* 作为主键关联到角色、光锥或道具
    """
    PlayerSelectedRewardPack = "PlayerSelectedRewardPack"
    """3.0 新增"""
    RandomRewardGift = "RandomRewardGift"
    """随机多选一, 机制不明"""
    Recipe = "Recipe"
    """合成台配方"""
    TeamSpecificFoodBenefit = "TeamSpecificFoodBenefit"
    """
    食物效果, 往往是战斗增益或减益.
    当 UseMethod 为此时, 会通过 UseDataID 关联到 ItemUseData.json
    再通过对应 ItemUseData 对象的 UerParam 作为主键关联到 ItemBuffData.json
    具体数值通过 ItemBuffData 的 MazeBuffID 关联到 MazeBuff.json
    """
    TravelBrochurePasterUse = "TravelBrochurePasterUse"
    """匹诺康尼梦境护照上的剪贴纸"""
    TravelBrochureUse = "TravelBrochureUse"
    """梦境护照本身（只有一个道具）"""
    TreasureMap = "TreasureMap"
    """
    藏宝图, 一般是使用后带有额外文字或图片的书籍或者相册, 非消耗品
    当 UseMethod 为此时, 会通过 UseDataID 关联到 ItemCureInfoData.json
    """


class UseType(enum.Enum):
    Food = "Food"
    Formula = "Formula"
    Gift = "Gift"
    Treasure = "Treasure"


class SellType(enum.Enum):
    Destroy = "Destroy"
    Sell = "Sell"


class ItemList(Model):
    """用于展示一整排物品，比如掉落物等"""

    item_id: int
    item_num: int


class ItemConfig(Model):
    id_: int
    item_main_type: MainType | None = None
    item_sub_type: SubType
    inventory_display_tag: typing.Literal[1, 2, 3]
    rarity: Rarity
    purpose_type: int | None = None
    is_visible: typing.Annotated[bool, pydantic.Field(alias="isVisible")] = False
    item_name: Text | None = None
    item_desc: Text | None = None
    item_bg_desc: Text | None = None
    item_icon_path: str
    item_figure_icon_path: str
    item_currency_icon_path: str
    item_avatar_icon_path: str
    is_auto_use: bool = False  # 1.3 及之前，后面大概合并为 UseMethod 了
    pile_limit: int
    """堆叠上限"""
    use_method: UseMethod | None = None
    custom_data_list: list[int]
    return_item_id_list: list[ItemList]
    """道具拆分效果，比如光锥、遗器"""
    item_group: int | None = None
    sell_type: SellType | None = None
    is_show_red_dot: bool = False

    @property
    def id(self) -> int:
        return self.id_


class ItemPurpose(Model):
    id_: int
    purpose_text: Text

    @property
    def id(self) -> int:
        return self.id_
