import argparse
import collections.abc
import dataclasses
import itertools
import pathlib
import sys
import typing

import httpx
import pydantic

import gsz.sr.excel
import gsz.sr.view

T = typing.TypeVar("T")


class Data(pydantic.BaseModel, typing.Generic[T]):
    retcode: int
    message: str
    data: T


class AchievementSeries(pydantic.BaseModel):
    series_id: int
    name: str
    icon: pydantic.AnyHttpUrl
    cur: int
    max: int


class Achievement(pydantic.BaseModel):
    id: int
    icon: pydantic.AnyHttpUrl
    title: str
    desc: str
    hide_desc: str
    finished: bool
    wiki_page_id: int
    priority: int
    is_favour: bool
    rarity: gsz.sr.excel.achievement.Rarity
    is_hide: bool
    sub_achievements: tuple["Achievement", ...]


class CultivateAchievement(pydantic.BaseModel):
    achievement_series_list: tuple[AchievementSeries, ...]
    achievement_list: tuple[Achievement, ...]


def parse_arguments():
    @dataclasses.dataclass
    class Arguments:
        game: gsz.sr.GameData
        e_hkrpg_token: str
        series: gsz.sr.view.AchievementSeries | None

    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--base", type=pathlib.Path)
    _ = parser.add_argument("--e-hkrpg-token")
    _ = parser.add_argument("--series")
    arguments = parser.parse_args()
    if arguments.e_hkrpg_token.startswith("@"):
        with open(arguments.e_hkrpg_token.removeprefix("@")) as secret:
            e_hkrpg_token = secret.read().strip()
    else:
        e_hkrpg_token: str = arguments.e_hkrpg_token
    game = gsz.sr.GameData(arguments.base)
    series: gsz.sr.view.AchievementSeries | None = None
    if arguments.series is not None:
        series = next((series for series in game.achievement_series() if series.title == arguments.series), None)
        if series is None:
            series_names = tuple(series.title for series in game.achievement_series())
            sys.exit(f"不存在成就系列：{series}，可能的成就系列为：{'、'.join(series_names)}")
    return Arguments(game=game, e_hkrpg_token=e_hkrpg_token, series=series)


def cultivate_achievement(e_hkrpg_token: str) -> tuple[Achievement, ...]:
    URL = "https://act-api-takumi.mihoyo.com/event/rpgcultivate/achievement/list"
    res = httpx.get(URL, params={"show_hide": True, "page_size": 10000}, cookies={"e_hkrpg_token": e_hkrpg_token})
    res = Data[CultivateAchievement].model_validate_json(res.content)
    return res.data.achievement_list


def achievement_title_descs(achievement: gsz.sr.view.AchievementData, formatter: gsz.format.Formatter):
    HIDE_PREFIX = "<color=#8790abff>※"
    HIDE_SUFFIX = "</color>"
    title = formatter.format(achievement.title)
    lines = achievement.desc.split("\\n")
    assert len(lines) == 1 or (
        len(lines) == 2 and lines[1].startswith(HIDE_PREFIX) and lines[1].endswith(HIDE_SUFFIX)
    ), f"成就描述应当只有一行，或者第二行被 {HIDE_PREFIX} {HIDE_SUFFIX} 包围"
    desc = formatter.format(lines[0], achievement.params)
    hide_desc: str | None = None
    if len(lines) == 2:
        hide_desc = lines[1].removeprefix(HIDE_PREFIX).removesuffix(HIDE_SUFFIX)
        hide_desc = formatter.format(hide_desc)
    return title, desc, hide_desc


def assemble_wikitext(
    game: gsz.sr.GameData,
    achievement: gsz.sr.view.AchievementData,
    sub_achievement_map: dict[int, tuple[int, ...]],
    avatars: collections.abc.Sequence[gsz.sr.view.AvatarConfig] = (),
    monsters: collections.abc.Sequence[gsz.sr.view.MonsterConfig] = (),
):
    formatter = gsz.format.Formatter(game=game, syntax=gsz.format.Syntax.MediaWiki)
    wiki = ["成就"]

    titles: list[str] = []
    descs: list[str] = []
    hide_descs: list[str] = []
    for sub in game.achievement_data(sub_achievement_map[achievement.id]):
        title, desc, hide_desc = achievement_title_descs(sub, formatter)
        titles.append(title)
        descs.append(desc)
        if hide_desc is not None:
            hide_descs.append(hide_desc)
    title = "/".join(titles)
    wiki.append(title)
    desc = "/".join(descs)
    wiki.append("说明=" + desc)
    if len(hide_descs) != 0:
        hide_desc = "/".join(hide_descs)
        wiki.append("补充说明=" + hide_desc)
    match achievement.rarity:
        case gsz.sr.excel.achievement.Rarity.High:
            reward = 20
        case gsz.sr.excel.achievement.Rarity.Mid:
            reward = 10
        case gsz.sr.excel.achievement.Rarity.Low:
            reward = 5
    wiki.append(f"奖励={reward}")
    wiki.append("版本=")
    is_hidden = "是" if achievement.show_type is gsz.sr.excel.achievement.ShowType.ShowAfterFinish else "否"
    wiki.append("隐藏=" + is_hidden)
    if achievement.series_id in (7, 8):
        # 战意奔涌、不屈者的荣光
        relevant_avatars = [formatter.format(avatar.name) for avatar in avatars if avatar.name in achievement.desc]
        if len(relevant_avatars) != 0:
            wiki.append("角色=" + "、".join(relevant_avatars))
        relevant_monsters = [
            formatter.format(monster.wiki_name) for monster in monsters if monster.name in achievement.desc
        ]
        if len(relevant_monsters) != 0:
            wiki.append("敌人=" + "、".join(relevant_monsters))
    wiki.append("注释=")
    wiki.append("攻略=")
    return "{{" + "|".join(wiki) + "}}"


def main():
    arguments = parse_arguments()
    sub_achievement_map = {
        achv.id: tuple(sub.id for sub in itertools.chain((achv,), achv.sub_achievements))
        for achv in cultivate_achievement(arguments.e_hkrpg_token)
    }
    achievements = arguments.game.achievement_data()
    if arguments.series is not None:
        achievements = (achievement for achievement in achievements if achievement.series_id == arguments.series.id)
    achievements = list(achievements)
    achievements.sort(key=lambda achievement: -achievement.priority)
    # 用于判断成就是否必要特定角色和敌人
    avatars = tuple(itertools.chain(arguments.game.avatar_config(), arguments.game.avatar_config_ld()))
    monster_name_dedup = set[str]()
    monster_prototypes = [monster.prototype() for monster in arguments.game.monster_config()]
    monsters = tuple(
        monster_name_dedup.add(prototype.name) or prototype
        for prototype in monster_prototypes
        if prototype.name != "" and prototype.name not in monster_name_dedup
    )

    for achievement in achievements:
        if achievement.id not in sub_achievement_map:
            continue
        print(assemble_wikitext(arguments.game, achievement, sub_achievement_map, avatars, monsters))


if __name__ == "__main__":
    main()
