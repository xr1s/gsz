from __future__ import annotations

import functools
import itertools
import typing

from .. import excel
from ..excel import avatar
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from ..excel import Element, Path
    from .item import ItemConfig


class AtlasAvatarChangeInfo(View[excel.AtlasAvatarChangeInfo]):
    ExcelOutput: typing.Final = excel.AtlasAvatarChangeInfo

    @functools.cached_property
    def __camp(self) -> AvatarCamp:
        camp = self._game.avatar_camp(self._excel.camp_id)
        assert camp is not None
        return camp

    def camp(self) -> AvatarCamp:
        return AvatarCamp(self._game, self.__camp._excel)


class AvatarAtlas(View[excel.AvatarAtlas]):
    ExcelOutput: typing.Final = excel.AvatarAtlas

    @functools.cached_property
    def cv_cn(self) -> str:
        return self._game.text(self._excel.cv_cn)

    @functools.cached_property
    def cv_jp(self) -> str:
        return self._game.text(self._excel.cv_jp)

    @functools.cached_property
    def cv_en(self) -> str | None:
        return self._game.text(self._excel.cv_en) if self._excel.cv_en is not None else ""

    @functools.cached_property
    def cv_kr(self) -> str | None:
        return self._game.text(self._excel.cv_kr)

    @functools.cached_property
    def __camp(self) -> AvatarCamp:
        camp = self._game.avatar_camp(self._excel.camp_id)
        assert camp is not None
        return camp

    def camp(self) -> AvatarCamp:
        return AvatarCamp(self._game, self.__camp._excel)


class AvatarCamp(View[excel.AvatarCamp]):
    ExcelOutput: typing.Final = excel.AvatarCamp

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)


class AvatarConfig(View[excel.AvatarConfig]):
    ExcelOutput: typing.Final = excel.AvatarConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.avatar_name)

    @functools.cached_property
    def full_name(self) -> str:
        return self._game.text(self._excel.avatar_full_name)

    @functools.cached_property
    def english_name(self) -> str:
        from ..data import Language

        name = self._game.text(self._excel.avatar_name, language=Language.EN)
        return name.replace("{NICKNAME}", "Trailblazer")

    @property
    def rarity(self) -> int:
        match self._excel.rarity:
            case avatar.Rarity.Type4:
                return 4
            case avatar.Rarity.Type5:
                return 5

    @functools.cached_property
    def __manikin(self) -> avatar.ManikinAvatar:
        path = self._game.base / self._excel.manikin_json_path
        return avatar.ManikinAvatar.model_validate_json(path.read_bytes())

    @property
    def is_male(self) -> bool:
        return self.body_size in (avatar.CharacterBodySize.Lad, avatar.CharacterBodySize.Boy, None)

    @property
    def body_size(self) -> avatar.CharacterBodySize | None:
        return self.__manikin.character_body_size

    @property
    def base_type(self) -> Path:
        return self._excel.avatar_base_type

    @property
    def damage_type(self) -> Element:
        return self._excel.damage_type

    @functools.cached_property
    def __ranks(self) -> list[AvatarRankConfig]:
        return list(self._game.avatar_rank_config(self._excel.rank_id_list))

    def ranks(self) -> collections.abc.Iterable[AvatarRankConfig]:
        return (AvatarRankConfig(self._game, rank._excel) for rank in self.__ranks)

    @functools.cached_property
    def __atlas(self) -> AvatarAtlas | None:
        return self._game.avatar_atlas(self._excel.avatar_id)

    def atlas(self) -> AvatarAtlas | None:
        return AvatarAtlas(self._game, self.__atlas._excel) if self.__atlas is not None else None

    @functools.cached_property
    def __atlas_change_info(self) -> AtlasAvatarChangeInfo | None:
        change = self._game._atlas_change_info_avatar_config.get(self._excel.avatar_id)  # pyright: ignore[reportPrivateUsage]
        return AtlasAvatarChangeInfo(self._game, change) if change is not None else None

    @functools.cached_property
    def __player_icon(self) -> AvatarPlayerIcon:
        return AvatarPlayerIcon(self._game, self._game._avatar_config_to_player_icon[self._excel.avatar_id])  # pyright: ignore[reportPrivateUsage]

    def player_icon(self) -> AvatarPlayerIcon:
        return AvatarPlayerIcon(self._game, self.__player_icon._excel)

    @functools.cached_property
    def __skill_tree(self) -> list[AvatarSkillTreeConfig]:
        return [
            AvatarSkillTreeConfig(self._game, skill)
            for skill in self._game._avatar_config_skill_trees[self._excel.avatar_id]  # pyright: ignore[reportPrivateUsage]
        ]

    def skill_tree(self) -> collections.abc.Iterable[AvatarSkillTreeConfig]:
        return (AvatarSkillTreeConfig(self._game, skill._excel) for skill in self.__skill_tree)

    @functools.cached_property
    def __normal_skill_tree(self) -> list[AvatarSkillTreeConfig]:
        """普攻"""
        return [
            point for point in self.__skill_tree if point._excel.point_trigger_key is avatar.PointTriggerKey.PointNormal
        ]

    @functools.cached_property
    def __bp_skill_tree(self) -> list[AvatarSkillTreeConfig]:
        """战技"""
        return [
            point
            for point in self.__skill_tree
            if point._excel.point_trigger_key is avatar.PointTriggerKey.PointBPSkill
        ]

    @functools.cached_property
    def __ultra_skill_tree(self) -> list[AvatarSkillTreeConfig]:
        """终结技"""
        return [
            point for point in self.__skill_tree if point._excel.point_trigger_key is avatar.PointTriggerKey.PointUltra
        ]

    @functools.cached_property
    def __maze_skill_tree(self) -> list[AvatarSkillTreeConfig]:
        """秘技"""
        return [
            point for point in self.__skill_tree if point._excel.point_trigger_key is avatar.PointTriggerKey.PointMaze
        ]

    @functools.cached_property
    def __passive_skill_tree(self) -> list[AvatarSkillTreeConfig]:
        """秘技"""
        return [
            point
            for point in self.__skill_tree
            if point._excel.point_trigger_key is avatar.PointTriggerKey.PointPassive
        ]

    @functools.cached_property
    def __promotions(self) -> list[AvatarPromotionConfig]:
        return list(self._game.avatar_promotion_config(self._excel.avatar_id))

    def promotions(self) -> collections.abc.Iterable[AvatarPromotionConfig]:
        return (AvatarPromotionConfig(self._game, promotion._excel) for promotion in self.__promotions)

    @functools.cached_property
    def __item(self) -> ItemConfig:
        item = self._game.item_config_avatar(self._excel.avatar_id)
        assert item is not None
        return item

    def item(self) -> ItemConfig:
        from .item import ItemConfig

        return ItemConfig(self._game, self.__item._excel)

    @functools.cached_property
    def __stories(self) -> list[StoryAtlas]:
        return list(self._game.story_atlas(self._excel.avatar_id))

    def stories(self) -> collections.abc.Iterable[StoryAtlas]:
        return (StoryAtlas(self._game, story._excel) for story in self.__stories)

    def story(self, story_id: int) -> str:
        story = next((story for story in self.__stories if story._excel.story_id == story_id), None)
        return story.story if story is not None else ""

    def story_final(self, replace_id: int) -> str:
        story = next((story for story in self.__stories if story._excel.replace_id == replace_id), None)
        if story is None:
            story = next((story for story in self.__stories if story._excel.story_id == replace_id), None)
        return story.story if story is not None else ""

    # 需要手动录入，和 WIKI 同步
    __PATH_MATERIAL_CATEGORY: dict[int, str] = {
        110113: "毁灭1",  # 净世残刃
        110123: "巡猎1",  # 逐星之矢
        110133: "智识1",  # 智识之钥
        110143: "存护1",  # 琥珀的坚守
        110153: "虚无1",  # 沉沦黑曜
        110163: "同谐1",  # 群星乐章
        110173: "丰饶1",  # 永恒之花
        110183: "毁灭2",  # 月狂獠牙
        110193: "巡猎2",  # 逆时一击
        110203: "智识2",  # 精致色稿
        110213: "存护2",  # 神体琥珀
        110223: "虚无2",  # 焚天之魔
        110233: "同谐2",  # 天外乐章
        110243: "丰饶2",  # 万相果实
        110253: "记忆1",  # 阿赖耶华
    }

    def __path_material_wiki_category_name(self) -> str:
        # skill 是无序的，所以直接找升到最高级需要的材料，顺序肯定不会混乱
        points = sorted(self.__skill_tree, key=lambda skill: (skill._excel.level))
        material = points[-1].path_material()
        assert material is not None
        return self.__PATH_MATERIAL_CATEGORY[material._excel.id_]

    # 需要手动录入，和 WIKI 同步
    __LOOT_MATERIAL_CATEGORY: dict[int, str] = {
        111003: "原核",  # 蠢动原核
        111013: "虚卒",  # 践踏的意志
        112003: "铁卫",  # 铁卫勋章
        112013: "古代",  # 古代引擎
        113003: "永寿",  # 永寿荣枝
        113013: "工造",  # 工造浑心
        114003: "梦境",  # 造梦马达
        114013: "忆域",  # 欲念碎镜
        115003: "眷属",  # 荣耀洗礼身躯
        115013: "黑潮",  # 哀叹漫无止境
    }

    def __loot_material_wiki_category_name(self) -> str:
        material = self.__promotions[-2].loot_material()
        assert material is not None
        return self.__LOOT_MATERIAL_CATEGORY[material._excel.id_]

    @property
    def sp_need(self) -> int | None:
        return self._excel.sp_need.value if self._excel.sp_need is not None else None

    # 其实所有角色的系数是固定的，可以直接计算，不需要用到所有 promotion
    # https://nga.178.com/read.php?tid=35573789&rand=370
    # 但这里还是按照文件里的记录来逐个计算吧

    def hp(self, level: int, promotion: bool = False) -> float:
        assert 0 < level < 80 or level == 80 and not promotion, "角色等级不能超过 80 级"
        assert level
        index = 0
        max_level = 0
        hp = 0
        while level > self.__promotions[index].max_level or promotion and level >= self.__promotions[index].max_level:
            hp += (self.__promotions[index].max_level - max_level) * self.__promotions[index].hp_add
            max_level = self.__promotions[index].max_level
            index += 1
        return self.__promotions[index].hp_base + hp + (level - max_level - 1) * self.__promotions[index].hp_add

    def attack(self, level: int, promotion: bool = False) -> float:
        assert 0 < level < 80 or level == 80 and not promotion, "角色等级不能超过 80 级"
        assert level
        index = 0
        max_level = 0
        attack = 0
        while level > self.__promotions[index].max_level or promotion and level >= self.__promotions[index].max_level:
            attack += (self.__promotions[index].max_level - max_level) * self.__promotions[index].attack_add
            max_level = self.__promotions[index].max_level
            index += 1
        return (
            self.__promotions[index].attack_base
            + attack
            + (level - max_level - 1) * self.__promotions[index].attack_add
        )

    def defence(self, level: int, promotion: bool = False) -> float:
        assert 0 < level < 80 or level == 80 and not promotion, "角色等级不能超过 80 级"
        assert level
        index = 0
        max_level = 0
        defence = 0
        while level > self.__promotions[index].max_level or promotion and level >= self.__promotions[index].max_level:
            defence += (self.__promotions[index].max_level - max_level) * self.__promotions[index].defence_add
            max_level = self.__promotions[index].max_level
            index += 1
        return (
            self.__promotions[index].defence_base
            + defence
            + (level - max_level - 1) * self.__promotions[index].defence_add
        )

    def wiki(self) -> str:
        camp = self.__atlas.camp() if self.__atlas is not None else None
        change_camp = self.__atlas_change_info.camp() if self.__atlas_change_info is not None else None
        # 短信联系人，可能为空，比如丹恒饮月没有对应联系人
        contacts = self._game.message_contacts_config(self._excel.avatar_id)
        # 角色晋阶材料
        promotion_material_item = self.__promotions[-2].promotion_material()
        assert promotion_material_item is not None
        bonus_abilities = [
            skill for skill in self.__skill_tree if skill._excel.point_type is avatar.PointType.BonusAbility
        ]
        weekly_material = bonus_abilities[0].weekly_material()
        assert weekly_material is not None
        stories = [self.story(k) for k in range(2, 6)]
        stories_final = [self.story_final(k) for k in range(2, 6)]
        stat_bonuses = [skill for skill in self.__skill_tree if skill._excel.point_type is avatar.PointType.StatBonus]
        normal_skill = next(iter(self.__normal_skill_tree[-1].skills()))
        normal_skill_rated = itertools.chain(normal_skill.rated_ranks(), normal_skill.rated_skill_tree())
        bp_skill = next(iter(self.__bp_skill_tree[-1].skills()))
        bp_skill_rated = itertools.chain(bp_skill.rated_ranks(), bp_skill.rated_skill_tree())
        ultra_skill = next(iter(self.__ultra_skill_tree[-1].skills()))
        ultra_skill_rated = itertools.chain(ultra_skill.rated_ranks(), ultra_skill.rated_skill_tree())
        passive_skill = next(iter(self.__passive_skill_tree[-1].skills()))
        passive_skill_rated = itertools.chain(passive_skill.rated_ranks(), passive_skill.rated_skill_tree())
        main_page = self._game._template_environment.get_template("角色.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            avatar=self,
            atlas=self.__atlas,  # 角色配音演员、所属阵营
            change_camp=change_camp,  # 角色所属阵营变更信息
            camp=camp,  # 角色所属阵营
            item=self.__item,  # 角色介绍
            contacts=contacts,
            path_material_name=self.__path_material_wiki_category_name(),  # 角色行迹升级素材
            loot_material_name=self.__loot_material_wiki_category_name(),  # 角色行迹、晋阶素材
            promotion_material_name=promotion_material_item.name,  # 角色晋阶素材
            weekly_material_name=weekly_material.name,  # 周本材料
            stories=stories,  # 角色故事
            stories_final=stories_final,  # 角色故事
            promotions=self.__promotions,  # 晋阶
            ranks=self.__ranks,  # 命座
            bonus_abilities=bonus_abilities,  # 额外能力
            stat_bonuses=stat_bonuses,  # 属性加成
            normal_skill_tree=self.__normal_skill_tree,  # 普攻
            bp_skill_tree=self.__bp_skill_tree,  # 战技
            ultra_skill_tree=self.__ultra_skill_tree,  # 终结技
            passive_skill_tree=self.__passive_skill_tree,  # 天赋
            maze_skill_tree=self.__maze_skill_tree,  # 秘技
            normal_skill_rated=(rated.wiki_bonus_effect_name() for rated in normal_skill_rated),  # 普攻效果加成
            bp_skill_rated=(rated.wiki_bonus_effect_name() for rated in bp_skill_rated),  # 战技效果加成
            ultra_skill_rated=(rated.wiki_bonus_effect_name() for rated in ultra_skill_rated),  # 终结技效果加成
            passive_skill_rated=(rated.wiki_bonus_effect_name() for rated in passive_skill_rated),  # 终结技效果加成
        )
        voices = list(self._game.voice_atlas(self._excel.avatar_id))
        interactive_voices = sorted(
            (voice for voice in voices if not voice._excel.is_battle_voice), key=lambda voice: voice._excel.sort_id
        )
        combat_voices = sorted(
            (voice for voice in voices if voice._excel.is_battle_voice), key=lambda voice: voice._excel.sort_id
        )
        voices_page = self._game._template_environment.get_template("角色语音.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            avatar=self, interactive_voices=interactive_voices, combat_voices=combat_voices
        )
        return main_page + "\n\n" + voices_page


class AvatarPlayerIcon(View[excel.AvatarPlayerIcon]):
    ExcelOutput: typing.Final = excel.AvatarPlayerIcon

    @functools.cached_property
    def __item(self) -> ItemConfig:
        item = self._game.item_config_avatar_player_icon(self._excel.id_)
        assert item is not None
        return item

    def item(self) -> ItemConfig:
        from .item import ItemConfig

        return ItemConfig(self._game, self.__item._excel)


class AvatarPromotionConfig(View[excel.AvatarPromotionConfig]):
    ExcelOutput: typing.Final = excel.AvatarPromotionConfig

    @property
    def max_level(self) -> int:
        return self._excel.max_level

    @property
    def speed_base(self) -> int:
        return self._excel.speed_base.value

    @property
    def hp_base(self) -> float:
        return self._excel.hp_base.value

    @property
    def hp_add(self) -> float:
        return self._excel.hp_add.value

    @property
    def attack_base(self) -> float:
        return self._excel.attack_base.value

    @property
    def attack_add(self) -> float:
        return self._excel.attack_add.value

    @property
    def defence_base(self) -> float:
        return self._excel.defence_base.value

    @property
    def defence_add(self) -> float:
        return self._excel.defence_add.value

    @functools.cached_property
    def __materials(self) -> list[ItemConfig]:
        materials: list[ItemConfig] = []
        for pair in self._excel.promotion_cost_list:
            item = self._game.item_config(pair.item_id)
            assert item is not None
            materials.append(item)
        return materials

    @functools.cached_property
    def __loot_material(self) -> ItemConfig | None:
        return next(material for material in self.__materials if material._excel.purpose_type == 7)

    def loot_material(self) -> ItemConfig | None:
        """命途相关的材料，刷赤色拟造花萼获取"""
        from .item import ItemConfig

        return ItemConfig(self._game, self.__loot_material._excel) if self.__loot_material is not None else None

    @functools.cached_property
    def __promotion_material(self) -> ItemConfig | None:
        return next((material for material in self.__materials if material._excel.purpose_type == 2), None)

    def promotion_material(self) -> ItemConfig | None:
        """突破材料，30 体力大世界精英怪素材"""
        from .item import ItemConfig

        return (
            ItemConfig(self._game, self.__promotion_material._excel) if self.__promotion_material is not None else None
        )


class AvatarRankConfig(View[excel.AvatarRankConfig]):
    ExcelOutput: typing.Final = excel.AvatarRankConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.desc)

    @functools.cached_property
    def param(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param)

    def wiki_bonus_effect_name(self) -> str:
        return f"星魂{self._excel.rank}"


class AvatarSkillConfig(View[excel.AvatarSkillConfig]):
    ExcelOutput: typing.Final = excel.AvatarSkillConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.skill_name)

    @functools.cached_property
    def tag(self) -> str:
        return self._game.text(self._excel.skill_tag)

    @functools.cached_property
    def type_desc(self) -> str:
        return self._game.text(self._excel.skill_type_desc)

    @property
    def desc(self) -> str | None:
        return self._game.text(self._excel.skill_desc) if self._excel.skill_desc is not None else None

    @property
    def param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)

    @property
    def bp_add(self) -> int:
        need = self._excel.bp_need.value if self._excel.bp_need is not None else 0
        if need != -1:
            return -need
        return self._excel.bp_add.value if self._excel.bp_add is not None else 0

    @property
    def sp_base(self) -> int | None:
        return self._excel.sp_base.value if self._excel.sp_base is not None else None

    @property
    def stance_damage_display(self) -> int | None:
        return self._excel.stance_damage_display

    @functools.cached_property
    def __rated_skill_tree(self) -> list[AvatarSkillTreeConfig]:
        points: list[AvatarSkillTreeConfig] = []
        for point_id in self._excel.rated_skill_tree_id:
            point = self._game.avatar_skill_tree_config(point_id, 1)
            assert point is not None
            points.append(point)
        return points

    def rated_skill_tree(self) -> collections.abc.Iterable[AvatarSkillTreeConfig]:
        return (AvatarSkillTreeConfig(self._game, point._excel) for point in self.__rated_skill_tree)

    @functools.cached_property
    def __rated_ranks(self) -> list[AvatarRankConfig]:
        ranks: list[AvatarRankConfig] = []
        for rank_id in self._excel.rated_rank_id:
            rank = self._game.avatar_rank_config(rank_id)
            assert rank is not None
            ranks.append(rank)
        return ranks

    def rated_ranks(self) -> collections.abc.Iterable[AvatarRankConfig]:
        return (AvatarRankConfig(self._game, rank._excel) for rank in self.__rated_ranks)


class AvatarSkillTreeConfig(View[excel.AvatarSkillTreeConfig]):
    ExcelOutput: typing.Final = excel.AvatarSkillTreeConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.point_name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.point_desc)

    @functools.cached_property
    def param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)

    @property
    def level(self) -> int:
        return self._excel.level

    @functools.cached_property
    def __skills(self) -> list[AvatarSkillConfig]:
        skills: list[AvatarSkillConfig] = []
        for skill_id in self._excel.level_up_skill_id:
            skill = self._game.avatar_skill_config(skill_id, self._excel.level)
            if skill is None:
                skill = self._game.avatar_servant_skill_config(skill_id, self._excel.level)
                assert skill is not None
            skills.append(skill)
        return skills

    def skills(self) -> collections.abc.Iterable[AvatarSkillConfig]:
        return (AvatarSkillConfig(self._game, skill._excel) for skill in self.__skills)

    def status_add_list(self) -> list[tuple[avatar.PropertyType, float]]:
        return [(add.property_type, add.value.value) for add in self._excel.status_add_list]

    @functools.cached_property
    def __materials(self):
        result: list[tuple[ItemConfig, int]] = []
        for item_pair in self._excel.material_list:
            item = self._game.item_config(item_pair.item_id)
            assert item is not None
            result.append((item, item_pair.item_num or 1))
        return result

    @functools.cached_property
    def __path_material(self) -> ItemConfig | None:
        return next((material for material, _num in self.__materials if material._excel.purpose_type == 3), None)

    def path_material(self) -> ItemConfig | None:
        """命途相关、同时是光锥晋阶材料的行迹材料，需要用开拓力刷赤色拟造花萼得到的材料"""
        from .item import ItemConfig

        return ItemConfig(self._game, self.__path_material._excel) if self.__path_material is not None else None

    @functools.cached_property
    def __loot_material(self) -> ItemConfig | None:
        return next((material for material, _num in self.__materials if material._excel.purpose_type == 7), None)

    def loot_material(self) -> ItemConfig | None:
        """野怪掉落的材料，同时是角色晋阶材料的行迹材料"""
        from .item import ItemConfig

        return ItemConfig(self._game, self.__loot_material._excel) if self.__loot_material is not None else None

    @functools.cached_property
    def __weekly_material(self) -> ItemConfig | None:
        return next((material for material, _num in self.__materials if material._excel.purpose_type == 4), None)

    def weekly_material(self) -> ItemConfig | None:
        """周本材料，同时是角色晋阶材料的行迹材料"""
        from .item import ItemConfig

        return ItemConfig(self._game, self.__weekly_material._excel) if self.__weekly_material is not None else None

    def wiki_bonus_effect_name(self) -> str:
        match self._excel.point_trigger_key:
            case avatar.PointTriggerKey.PointB1:
                return "额外能力1"
            case avatar.PointTriggerKey.PointB2:
                return "额外能力2"
            case avatar.PointTriggerKey.PointB3:
                return "额外能力3"
            case _:
                return ""


class StoryAtlas(View[excel.StoryAtlas]):
    ExcelOutput: typing.Final = excel.StoryAtlas

    @functools.cached_property
    def story(self) -> str:
        return self._game.text(self._excel.story)


class VoiceAtlas(View[excel.VoiceAtlas]):
    ExcelOutput: typing.Final = excel.VoiceAtlas

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.voice_title)

    @functools.cached_property
    def chinese(self) -> str:
        return self._game.text(self._excel.voice_m)

    @functools.cached_property
    def japanese(self) -> str:
        from ..data import Language

        return self._game.text(self._excel.voice_m, language=Language.JP)

    @functools.cached_property
    def english(self) -> str:
        from ..data import Language

        return self._game.text(self._excel.voice_m, language=Language.EN)

    @functools.cached_property
    def korean(self) -> str:
        from ..data import Language

        return self._game.text(self._excel.voice_m, language=Language.KR)
