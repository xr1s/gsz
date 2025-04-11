from __future__ import annotations
import functools
import typing

from .. import excel
from ..excel import planet_fes
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from .avatar import AvatarConfig
    from .item import ItemConfig


class PlanetFesAvatar(View[excel.PlanetFesAvatar]):
    ExcelOutput: typing.Final = excel.PlanetFesAvatar

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @functools.cached_property
    def __rarity(self) -> PlanetFesAvatarRarity:
        rarity = self._game.planet_fes_avatar_rarity(self._excel.rarity.value)
        assert rarity is not None
        return rarity

    @property
    def rarity_value(self) -> int:
        return self._excel.rarity.value

    def rarity(self) -> PlanetFesAvatarRarity:
        return PlanetFesAvatarRarity(self._game, self.__rarity._excel)

    @property
    def planet_type(self) -> planet_fes.LandType:
        return self._excel.planet_type

    @functools.cached_property
    def __item(self) -> ItemConfig:
        item = self._game.item_config(self._excel.item_id)
        assert item is not None
        return item

    def item(self) -> ItemConfig:
        from .item import ItemConfig

        return ItemConfig(self._game, self.__item._excel)

    @functools.cached_property
    def __skills_1(self) -> list[PlanetFesBuff]:
        return list(self._game.planet_fes_avatar_buff(self._excel.skill_1_list))

    def skills_1(self) -> collections.abc.Iterable[PlanetFesBuff]:
        return (PlanetFesBuff(self._game, skill._excel) for skill in self.__skills_1)

    @functools.cached_property
    def __skills_2(self) -> list[PlanetFesBuff]:
        return list(self._game.planet_fes_avatar_buff(self._excel.skill_2_list))

    def skills_2(self) -> collections.abc.Iterable[PlanetFesBuff]:
        return (PlanetFesBuff(self._game, skill._excel) for skill in self.__skills_2)


class PlanetFesAvatarEvent(View[excel.PlanetFesAvatarEvent]):
    ExcelOutput: typing.Final = excel.PlanetFesAvatarEvent

    @functools.cached_property
    def event_content(self) -> str:
        return self._game.text(self._excel.event_content)

    @functools.cached_property
    def __avatar(self) -> AvatarConfig | None:
        if self._excel.avatar_id is None:
            return None
        avatar = self._game.avatar_config(self._excel.avatar_id)
        assert avatar is not None
        return avatar

    def avatar(self) -> AvatarConfig | None:
        from .avatar import AvatarConfig

        return None if self.__avatar is None else AvatarConfig(self._game, self.__avatar._excel)

    @functools.cached_property
    def __options(self) -> list[PlanetFesAvatarEventOption]:
        return list(self._game.planet_fes_avatar_event_option(self._excel.event_option_id_list))

    def options(self) -> collections.abc.Iterable[PlanetFesAvatarEventOption]:
        return (PlanetFesAvatarEventOption(self._game, option._excel) for option in self.__options)


class PlanetFesAvatarEventOption(View[excel.PlanetFesAvatarEventOption]):
    ExcelOutput: typing.Final = excel.PlanetFesAvatarEventOption

    @functools.cached_property
    def reward_pool_id(self) -> int | None:
        return self._excel.reward_pool_id

    @functools.cached_property
    def event_content(self) -> str:
        return self._game.text(self._excel.event_content)

    @functools.cached_property
    def option_bubble_talk(self) -> str:
        return self._game.text(self._excel.option_bubble_talk)

    @functools.cached_property
    def __next_options(self) -> list[PlanetFesAvatarEventOption]:
        return list(self._game.planet_fes_avatar_event_option(self._excel.next_option_list))

    def next_options(self) -> collections.abc.Iterable[PlanetFesAvatarEventOption]:
        return (PlanetFesAvatarEventOption(self._game, option._excel) for option in self.__next_options)

    @functools.cached_property
    def __reward(self) -> PlanetFesGameReward | None:
        if self._excel.activity_reward_id is None:
            return None
        reward = self._game.planet_fes_game_reward(self._excel.activity_reward_id)
        assert reward is not None
        return reward

    def reward(self) -> PlanetFesGameReward | None:
        return None if self.__reward is None else PlanetFesGameReward(self._game, self.__reward._excel)


class PlanetFesAvatarLevel(View[excel.PlanetFesAvatarLevel]):
    ExcelOutput: typing.Final = excel.PlanetFesAvatarLevel

    @property
    def level(self) -> int:
        return self._excel.level

    @property
    def cost_num(self) -> int:
        return int(self._excel.cost_num)

    @property
    def cost(self) -> str:
        return str(self._excel.cost_num)

    @property
    def income_num(self) -> int:
        return int(self._excel.income_num)

    @property
    def income(self) -> str:
        return str(self._excel.income_num)


class PlanetFesAvatarRarity(View[excel.PlanetFesAvatarRarity]):
    ExcelOutput: typing.Final = excel.PlanetFesAvatarRarity

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @property
    def cost_param(self) -> int:
        return self._excel.cost_param


class PlanetFesBuff(View[excel.PlanetFesBuff]):
    ExcelOutput: typing.Final = excel.PlanetFesBuff

    @functools.cached_property
    def __type(self) -> PlanetFesBuffType:
        typ = self._game.planet_fes_buff_type(self._excel.type.value)
        assert typ is not None
        return typ

    def type(self) -> PlanetFesBuffType:
        return PlanetFesBuffType(self._game, self.__type._excel)

    @property
    def description(self) -> str:
        return self.__type.description

    @property
    def params(self) -> tuple[int | str, ...]:
        param0: str | int
        match self._excel.type:
            case planet_fes.BuffType.IncomeIncreaseIfAvatarIdMatch:
                avatar = self._game.planet_fes_avatar(self._excel.type_param[0])
                assert avatar is not None
                param0 = avatar.name
            case planet_fes.BuffType.IncomeIncreaseIfLandTypeMatch:
                land = list(self._game.planet_fes_land_type())[self._excel.type_param[0] - 1]
                param0 = land.name
            case _:
                param0 = self._excel.type_param[0]
        return (param0, *self._excel.type_param[1:])


class PlanetFesBuffType(View[excel.PlanetFesBuffType]):
    ExcelOutput: typing.Final = excel.PlanetFesBuffType

    @functools.cached_property
    def description(self) -> str:
        return self._game.text(self._excel.decription)


class PlanetFesCard(View[excel.PlanetFesCard]):
    ExcelOutput: typing.Final = excel.PlanetFesCard

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @property
    def rarity(self) -> typing.Literal[1, 2]:
        return self._excel.rarity

    @functools.cached_property
    def description(self) -> str:
        return self._game.text(self._excel.description)

    @functools.cached_property
    def __buffs(self) -> list[PlanetFesBuff]:
        return list(self._game.planet_fes_buff(self._excel.buff_id_list))

    def buffs(self) -> collections.abc.Iterable[PlanetFesBuff]:
        return (PlanetFesBuff(self._game, buff._excel) for buff in self.__buffs)


class PlanetFesCardTheme(View[excel.PlanetFesCardTheme]):
    ExcelOutput: typing.Final = excel.PlanetFesCardTheme

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @functools.cached_property
    def __cards(self) -> list[PlanetFesCard]:
        return list(self._game.planet_fes_card(self._excel.card_id_list))

    def cards(self) -> collections.abc.Iterable[PlanetFesCard]:
        return (PlanetFesCard(self._game, card._excel) for card in self.__cards)


class PlanetFesFinishway(View[excel.PlanetFesFinishway]):
    ExcelOutput: typing.Final = excel.PlanetFesFinishway

    def params(self) -> tuple[int | str, ...]:  # noqa: PLR0911
        match self._excel.finish_type:
            case planet_fes.FinishType.AvatarBuffEffectiveWithIDList:
                return tuple(avatar.name for avatar in self._game.planet_fes_avatar(self._excel.param_int_list))
            case planet_fes.FinishType.AvatarDynamicLevel:
                assert self._excel.param_int_1 is not None
                assert self._excel.param_int_2 is not None
                assert self._excel.param_int_3 is not None
                avatar = self._game.planet_fes_avatar(self._excel.param_int_3)
                assert avatar is not None
                return (avatar.name, "???")
            case planet_fes.FinishType.AvatarLevel:
                assert self._excel.param_int_1 is not None
                assert self._excel.param_int_2 is not None
                avatar = self._game.planet_fes_avatar(self._excel.param_int_1)
                assert avatar is not None
                return (avatar.name, self._excel.param_int_2)
            case planet_fes.FinishType.AvatarNumWithLevel:
                assert self._excel.param_int_1 is not None
                return (self._excel.param_int_1, self._excel.progress)
            case planet_fes.FinishType.ConsumeItemNumWithType | planet_fes.FinishType.DoGachaCnt:
                return (self._excel.progress,)
            case planet_fes.FinishType.DynamicProfitRate:
                assert self._excel.param_int_1
                return ("???",)
            case planet_fes.FinishType.ProfitPerSecond:
                assert self._excel.param_int_1 is not None
                return (str(planet_fes.Num.from_int(self._excel.param_int_1)),)
            case planet_fes.FinishType.WorkAvatarDynamicLevel:
                assert self._excel.param_int_1 is not None
                return (self._excel.progress, self._excel.param_int_1)
            case _:
                assert self._excel.param_int_1 is not None
                params: list[int] = [self._excel.param_int_1]
                if self._excel.param_int_2 is not None:
                    params.append(self._excel.param_int_2)
                if self._excel.param_int_3 is not None:
                    params.append(self._excel.param_int_3)
                return tuple(params)

    def comment(self) -> str | None:
        match self._excel.finish_type:
            case planet_fes.FinishType.AvatarDynamicLevel:
                assert self._excel.param_int_1 is not None
                assert self._excel.param_int_2 is not None
                assert self._excel.param_int_3 is not None
                avatar = self._game.planet_fes_avatar(self._excel.param_int_3)
                assert avatar is not None
                return f"(当前每秒收益 &times; {self._excel.param_int_1 // 10}分钟)全部投入{avatar.name}达到的等级<br />按{self._excel.param_int_2}的倍数向上取整"
            case planet_fes.FinishType.DynamicProfitRate:
                assert self._excel.param_int_1
                return f"当前每秒收益*{self._excel.param_int_1}%"
            case _:
                return None


class PlanetFesGameReward(View[excel.PlanetFesGameReward]):
    ExcelOutput: typing.Final = excel.PlanetFesGameReward

    @property
    def gold_num(self) -> int | None:
        return self._excel.gold_num

    @functools.cached_property
    def __items(self) -> list[tuple[ItemConfig, int]]:
        items: list[tuple[ItemConfig, int]] = []
        for item_id, num in self._excel.item_list.items():
            item = self._game.item_config(item_id)
            assert item is not None
            items.append((item, num))
        return items

    def items(self) -> collections.abc.Iterable[tuple[ItemConfig, int]]:
        from .item import ItemConfig

        return ((ItemConfig(self._game, item._excel), num) for item, num in self.__items)


class PlanetFesGameRewardPool(View[excel.PlanetFesGameRewardPool]):
    ExcelOutput: typing.Final = excel.PlanetFesGameRewardPool

    @functools.cached_property
    def __rewards(self) -> list[PlanetFesGameReward]:
        return list(self._game.planet_fes_game_reward(self._excel.reward_param.values()))

    def rewards(self) -> collections.abc.Iterable[PlanetFesGameReward]:
        return (PlanetFesGameReward(self._game, reward._excel) for reward in self.__rewards)


class PlanetFesLandType(View[excel.PlanetFesLandType]):
    ExcelOutput: typing.Final = excel.PlanetFesLandType

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)


class PlanetFesQuest(View[excel.PlanetFesQuest]):
    ExcelOutput: typing.Final = excel.PlanetFesQuest

    @functools.cached_property
    def name(self) -> str | None:
        return None if self._excel.name is None else self._game.text(self._excel.name)

    @property
    def type(self) -> planet_fes.QuestType:
        return self._excel.quest_type

    @functools.cached_property
    def description(self) -> str:
        return self._game.text(self._excel.description)

    @functools.cached_property
    def __finishway(self) -> PlanetFesFinishway:
        finishway = self._game.planet_fes_finishway(self._excel.finishway_id)
        assert finishway is not None
        return finishway

    def finishway(self) -> PlanetFesFinishway:
        return PlanetFesFinishway(self._game, self.__finishway._excel)

    @functools.cached_property
    def __reward_items(self) -> list[tuple[ItemConfig, int]]:
        rewards: list[tuple[ItemConfig, int]] = []
        for element in self._excel.reward_item_list:
            item = self._game.item_config(element.item_id)
            assert item is not None
            rewards.append((item, element.item_num))
        return rewards

    def reward_items(self) -> collections.abc.Iterable[tuple[ItemConfig, int]]:
        from .item import ItemConfig

        return ((ItemConfig(self._game, item._excel), num) for item, num in self.__reward_items)
