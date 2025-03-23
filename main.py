import itertools
import pathlib
import textwrap
import typing

import fire

import gsz.format
import gsz.sr
from gsz.sr.excel import Text
import gsz.sr.view


def confirm_excel_objects_validate_no_error(game: gsz.sr.GameData):
    for val in dir(game):
        if val in ("_GameData__text_map", "text", "base"):
            continue
        if val.startswith("_"):
            continue
        print(val, getattr(game, val)())


@typing.final
class Main:
    def __init__(self, base: pathlib.Path | str):
        assert isinstance(base, pathlib.Path | str)
        self.base = base
        self.__game = gsz.sr.GameData(base)
        self.__formatter = gsz.format.Formatter(game=self.__game, syntax=gsz.format.Syntax.Terminal)

    def monster(self, name: str | None = None):
        if name is not None:
            assert isinstance(name, str)
            for monster in self.__game.monster_config_name(name):
                print(monster.wiki(), end="\n\n")
            return
        for monster in self.__game.monster_config():
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

    def event(self, title: str):
        """模拟宇宙事件"""
        assert isinstance(title, str)
        events = self.__game.rogue_tourn_hand_book_event_name(title)
        wikis: list[str] = []
        for event in events:
            for dialogue in event.dialogues():
                print(dialogue.dialogue_path)
                wikis.append(dialogue.wiki())
        if len(wikis) == 2:
            if wikis[0] == wikis[1]:
                print("差分宇宙", wikis[0], end="\n\n")
            else:
                print("人间喜剧:", wikis[0], end="\n\n")
                print("千面英雄:", wikis[1], end="\n\n")
        else:
            for wiki in wikis:
                print(textwrap.indent(wiki, "  "), end="\n\n")

        events = self.__game.rogue_hand_book_event_name(title)
        for event in events:
            types = list(event.types())
            for index, dialogue in enumerate(event.dialogues()):
                if index < len(types):
                    print(types[index].title)
                print(dialogue.dialogue_path)
                print(dialogue.wiki(), end="\n\n")

    def formula(self):
        pass

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

    def text(self, *hashes: int):
        print("\n".join(self.__game.text(Text(hash=hash)) for hash in hashes))

    def talk(self, *ids: int):
        for id in ids:
            talk = self.__game.talk_sentence_config(id)
            assert talk is not None
            print(f"{talk.name}：{talk.text}")

    def main(self):
        pass  # 调试代码可以放这里


if __name__ == "__main__":
    fire.Fire(Main)
