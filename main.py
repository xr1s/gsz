import datetime
import itertools
import pathlib
import textwrap
import typing

import fire

import gsz.format
import gsz.sr
import gsz.sr.excel
import gsz.sr.view


def confirm_excel_objects_validate_no_error(game: gsz.sr.GameData):
    for val in dir(game):
        if val in ("_GameData__text_map", "text", "base"):
            continue
        if val.startswith("_"):
            continue
        if val.endswith("_name"):
            continue
        print(val)
        getattr(game, val)()


@typing.final
class Main:
    def __init__(self, base: pathlib.Path | str):
        assert isinstance(base, pathlib.Path | str)
        self.base = base
        self.__game = gsz.sr.GameData(base)
        self.__formatter = gsz.format.Formatter(game=self.__game, syntax=gsz.format.Syntax.Terminal)

    def monster(self, name: str | None = None):
        monster_name_dedup = set[str]()
        prototypes = [monster.prototype() for monster in self.__game.monster_config()]
        prototypes = [
            monster_name_dedup.add(prototype.name) or prototype
            for prototype in prototypes
            if prototype.name not in monster_name_dedup
        ]
        for monster in prototypes:
            if name is not None and monster.name != name:
                continue
            print(monster.wiki(), end="\n\n")

    def miracle(self):
        dedup_miracle_names = set[str]()
        miracles = [
            dedup_miracle_names.add(miracle.name) or miracle
            for miracle in itertools.chain(
                self.__game.rogue_handbook_miracle(),
                self.__game.rogue_tourn_handbook_miracle(),
            )
            if miracle.name != "" and miracle.name not in dedup_miracle_names
        ]
        for miracle in miracles:
            print(miracle.wiki(), end="\n\n")

    def event(self, title: str, debug: bool = False):
        """模拟宇宙事件"""
        assert isinstance(title, str)
        events = self.__game.rogue_tourn_hand_book_event_name(title)
        wikis: list[str] = []
        for event in events:
            for dialogue in event.dialogues():
                print(dialogue.dialogue_path)
                print(dialogue.option_path)
                wikis.append(dialogue.wiki(debug))
        if len(wikis) == 2:
            if wikis[0] == wikis[1]:
                print("差分宇宙", wikis[0], end="\n\n")
            else:
                print("人间喜剧:", wikis[0], end="\n\n")
                print("千面英雄:", wikis[1], end="\n\n")
        else:
            for wiki in wikis:
                print(wiki, end="\n\n")

        events = self.__game.rogue_hand_book_event_name(title)
        for event in events:
            types = list(event.types())
            for index, dialogue in enumerate(event.dialogues()):
                if index < len(types):
                    print(types[index].title)
                print(dialogue.dialogue_path)
                print(dialogue.option_path)
                print(dialogue.wiki(debug), end="\n\n")

    def formula(self):
        for formula in self.__game.rogue_tourn_formula():
            print(formula.wiki(), end="\n\n")

    def rogue_buff(self):
        dedup_buff_names = set[str]()
        buffs = [
            dedup_buff_names.add(buff.name) or buff
            for buff in itertools.chain(self.__game.rogue_buff(), self.__game.rogue_tourn_buff())
            if buff.name != "" and buff.name not in dedup_buff_names
        ]
        for buff in buffs:
            print(buff.wiki(), end="\n\n")

    def extrapolation(self):
        """周期演算"""
        for challenge in self.__game.rogue_tourn_weekly_challenge():
            print(challenge.wiki(), end="\n\n")

    def book(self, title: str | None = None, pretty: bool = False):
        if title is not None:
            assert isinstance(title, str)
            for series in self.__game.book_series_config_name(title):
                if pretty:
                    for book in series.books():
                        print(self.__formatter.format(book.content))
                else:
                    print(series.wiki(), end="\n\n")
            return
        for series in self.__game.book_series_config():
            print(series.wiki(), end="\n\n")

    def text(self, *hashes: int):
        print("\n".join(self.__game.text(gsz.sr.excel.Text(hash=hash)) for hash in hashes))

    def talk(self, *ids: int):
        for id in ids:
            talk = self.__game.talk_sentence_config(id)
            assert talk is not None
            print(f"{talk.name}：{talk.text}")

    def message(self, contacts_name: str | None = None, section_id: int | None = None):
        if section_id is not None:
            assert isinstance(section_id, int)
            section = self.__game.message_section_config(section_id)
            if section is not None:
                print(section.wiki())
            return
        if contacts_name is not None:
            assert isinstance(contacts_name, str)
        for contacts in self.__game.message_contacts_config():
            if contacts_name is not None and self.__formatter.format(contacts.name) != contacts_name:
                continue
            print(contacts.wiki(), end="\n\n")

    def rogue_npc(self):
        for npc in itertools.chain(
            self.__game.rogue_npc(), self.__game.rogue_tourn_npc(), self.__game.rogue_magic_npc()
        ):
            for dialogue in npc.dialogue_list():
                print(npc.name, dialogue.dialogue_path, end=" ")
                print(
                    dialogue.wiki(debug=True),
                    end="\n\n",
                )

    def challenge(
        self,
        type: typing.Literal["memory", "story", "boss"] | None = None,
        current: bool = False,
        next: bool = False,
        date: str | None = None,
    ):
        assert isinstance(current, bool)
        assert isinstance(next, bool)
        assert type in (None, "memory", "story", "boss")
        challenges: list[gsz.sr.view.ChallengeGroupConfig] = []
        if type == "memory" or type is None:
            challenges.extend(self.__game.challenge_group_config())
        if type == "story" or type is None:
            challenges.extend(self.__game.challenge_story_group_config())
        if type == "boss" or type is None:
            challenges.extend(self.__game.challenge_boss_group_config())
        ask_datetime: datetime.datetime | None = None
        if date is not None:
            assert isinstance(date, str)
            assert not current
            assert not next
            dt = datetime.datetime.strptime(date, "%Y-%m-%d").date()  # noqa: DTZ007
            ask_datetime = datetime.datetime.combine(dt, datetime.time(4))
        if next or current:
            assert current != next  # != 是异或，这里意思为 current 或 next 只有一个可以为 True
            ask_datetime = datetime.datetime.now()  # noqa: DTZ005
            ask_datetime = ask_datetime + datetime.timedelta(days=42 if next else 0)
        for challenge in challenges:
            sched = challenge.schedule()
            if ask_datetime is not None and (sched is None or not sched.contains(ask_datetime)):
                continue
            print(challenge.wiki(), end="\n\n")

    def planet_fes(self, q: typing.Literal["avatar", "achievement", "task", "event", "card"]):  # noqa: PLR0912, PLR0915
        assert q in ("avatar", "achievement", "task", "event", "card")
        formatter = gsz.format.Formatter(game=self.__game, syntax=gsz.format.Syntax.MediaWiki, percent_as_plain=True)
        match q:
            case "avatar":
                avatars = sorted(self.__game.planet_fes_avatar(), key=lambda avatar: (-avatar.rarity_value, -avatar.id))
                for avatar in avatars:
                    rarity = avatar.rarity()
                    skills_1 = list(avatar.skills_1())
                    skill_descriptions: list[str] = [formatter.format(skills_1[0].description, skills_1[0].params)]
                    skills_2 = list(avatar.skills_2())
                    if len(skills_2) != 0:
                        skill_descriptions.append(formatter.format(skills_2[0].description, skills_2[0].params))
                    skill_description = "".join("\n* " + description for description in skill_descriptions)
                    detail = textwrap.dedent(f"""\
                        {{{{:「星铁☆WORLD」/助理|{avatar.name}|
                        |工作技巧={rarity.name}
                        |工作展区={avatar.planet_type}
                        |介绍=
                        |助理特质={textwrap.indent(skill_description, "                    ")}
                        }}}}""")
                    print(detail, end="\n\n")
            case "achievement":
                print('{| id="achievement" class="wikitable"')
                print("! 成就 !! 等级 !! 描述 !! 奖励")
                counter = 0
                for quest in self.__game.planet_fes_quest():
                    if quest.type is gsz.sr.excel.planet_fes.QuestType.Task:
                        continue
                    counter = counter % 5 + 1
                    print("|-")
                    print("|", quest.name, "||", counter, end=" ")
                    print("||", formatter.format(quest.description, quest.finishway().params()), end=" ")
                    print("||", "、".join(f"{{{{图标|{item.name}|{num}}}}}" for item, num in quest.reward_items()))
                print("|}")
            case "card":
                for theme in self.__game.planet_fes_card_theme():
                    cards = list(theme.cards())
                    cards.sort(key=lambda card: -card.rarity)
                    for card in cards:
                        match card.rarity:
                            case 1:
                                rarity = "{{颜色|c1eeff|普通}}"
                            case 2:
                                rarity = "{{颜色|f4e7a8|稀有}}"
                        print(
                            f"|-\n| [[文件:星铁☆WORLD-回忆卡-{card.name}.png|256px]] || {card.name} || {theme.name} || {rarity} || ",
                            end="",
                        )
                        buffs = list(card.buffs())
                        assert len(buffs) == 1
                        print(formatter.format(buffs[0].description, buffs[0].params), end=" ")
                        print(f"|| {formatter.format(card.description)} <!-- {card._excel.pic_path} -->")
            case "task":
                for quest in self.__game.planet_fes_quest():
                    if quest.type is gsz.sr.excel.planet_fes.QuestType.Achievement:
                        continue
                    finishway = quest.finishway()
                    print("|-")
                    print("|", formatter.format(quest.description, finishway.params()), end="")
                    comment = finishway.comment()
                    if comment is not None:
                        print(f'<p style="color: #cbcbcb">※ {comment}</p>', end="")
                    print(" ", end="")
                    print("||", "、".join(f"{{{{图标|{item.name}|{num}}}}}" for item, num in quest.reward_items()))
            case "event":
                header = textwrap.dedent("""\
                    {| id="event" class="wikitable" style="width: 100%"
                    ! style="width: 0%"  | 角色
                    ! style="width: 20%" | 事件描述
                    ! style="width: 6%"  | 选择
                    ! style="width: 10%" | 选择描述
                    ! style="width: 4%"  | 稀有度<br>概率
                    ! style="width: 6%"  | 分支
                    ! style="width: 10%" | 分支描述
                    ! style="width: 5%"  | 奖励""")
                print(header)
                for e in self.__game.planet_fes_avatar_event():
                    rowspan = sum(max(1, sum(1 for _ in option.next_options())) for option in e.options())
                    character = e.avatar()
                    character_icon = "" if character is None else f"{{{{图标|大|{character.name}}}}}"
                    print(f'|- class="sep"\n| rowspan="{rowspan}" | {character_icon}')
                    print(f'| rowspan="{rowspan}" | {formatter.format(e.event_content)}')
                    for option_index, option in enumerate(e.options()):
                        if option_index != 0:
                            print("|-")
                        rowspan = max(1, sum(1 for _ in option.next_options()))
                        print(f'| rowspan="{rowspan}" | {formatter.format(option.event_content)}')  # 选项
                        print(f'| rowspan="{rowspan}" | {formatter.format(option.option_bubble_talk)}')  # 选项剧情
                        rolls = list(option.next_options())
                        for roll_index, roll in enumerate(rolls):
                            if roll_index != 0:
                                print("|-")
                            assert roll.reward_pool_id is not None
                            rarity = ["", "SSS", "SS", "S", "A", "B"][roll.reward_pool_id]
                            possibility = [30, 30, 40] if len(rolls) == 3 else [40, 60]
                            print(f'| class="mid" | {rarity}<br>{possibility[roll_index]}%', end=" ")
                            print("||", formatter.format(roll.event_content), end=" ")  # 骰子结果
                            print("||", formatter.format(roll.option_bubble_talk), "||", end="\n")  # 骰子剧情
                print("|}")

    def main(self):
        """调试代码可以放这里"""


if __name__ == "__main__":
    fire.Fire(Main)
