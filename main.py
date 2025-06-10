import datetime
import difflib
import io
import itertools
import logging
import pathlib
import re
import textwrap
import typing
import zoneinfo

import aiofiles
import aiofiles.os
import fire

import gsz.bbs
import gsz.format
import gsz.sr
import gsz.sr.excel
import gsz.sr.view
import gsz.zzz


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
    def __init__(self, base: pathlib.Path | str | None = None):
        self.__game = None
        if base is None:
            return  # 可能是下载社媒，不需要提供 GameData 路径
        assert isinstance(base, pathlib.Path | str)
        self.base = pathlib.Path(base)
        if self.base.joinpath("ExcelBinOutput").exists():  # Genshin Impact
            raise NotImplementedError("AnimeGameData not implemented")
        if self.base.joinpath("ExcelOutput").exists():
            self.__game = gsz.sr.GameData(base)
        if self.base.joinpath("FileCfg").exists():
            self.__game = gsz.zzz.GameData(base)
        self.__formatter = gsz.format.Formatter(game=self.__game, syntax=gsz.format.Syntax.Terminal)
        self.__mwformatter = gsz.format.Formatter(game=self.__game, syntax=gsz.format.Syntax.MediaWiki)

    def monster(self, name: str | None = None):
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> monster` required"
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
        """模拟宇宙 / 差分宇宙 奇物"""
        assert isinstance(self.__game, gsz.sr.GameData), "`--base TurnBasedGameData> miracle` required"
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

    def rogue_event(self, title: str | None = None, debug: bool = False):
        """模拟宇宙事件"""
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> rogue-event` required"
        if title is not None:
            assert isinstance(title, str)
            events = self.__game.rogue_hand_book_event_name(title)
            for event in events:
                types = list(event.types())
                for index, dialogue in enumerate(event.dialogues()):
                    if index < len(types):
                        print(types[index].title)
                    print(dialogue.dialogue_path)
                    print(dialogue.option_path)
                    print(dialogue.wiki(debug=debug), end="\n\n")
            return
        for event in self.__game.rogue_hand_book_event():
            print(event.name, end="")
            for dialogue in event.dialogues():
                print(dialogue.wiki(debug=debug), end="\n\n")

    def rogue_tourn_event(self, title: str | None = None, debug: bool = False):
        """差分宇宙事件"""
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> rogue-tourn-event` required"
        if title is not None:
            assert isinstance(title, str)
            events = self.__game.rogue_tourn_hand_book_event_name(title)
            wikis: list[str] = []
            for event in events:
                for dialogue in event.dialogues():
                    print(dialogue.dialogue_path)
                    print(dialogue.option_path)
                    wikis.append(dialogue.wiki(debug=debug))
            if len(wikis) == 2:
                if wikis[0] == wikis[1]:
                    print("差分宇宙", wikis[0], end="\n\n")
                else:
                    print("人间喜剧:", wikis[0], end="\n\n")
                    print("千面英雄:", wikis[1], end="\n\n")
            else:
                for wiki in wikis:
                    print(wiki, end="\n\n")
            return
        for event in self.__game.rogue_tourn_hand_book_event():
            print(event.name, end="")
            for dialogue in event.dialogues():
                print(dialogue.wiki(debug=debug), end="\n\n")

    def formula(self):
        """差分宇宙方程"""
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> formula` required"
        for formula in self.__game.rogue_tourn_formula():
            print(formula.wiki(), end="\n\n")

    def rogue_buff(self):
        """模拟宇宙 / 差分宇宙 祝福"""
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> rogue-buff` required"
        dedup_buff_names = set[str]()
        buffs = [
            dedup_buff_names.add(buff.name) or buff
            for buff in itertools.chain(self.__game.rogue_buff(), self.__game.rogue_tourn_buff())
            if buff.name != "" and buff.name not in dedup_buff_names
        ]
        for buff in buffs:
            print(buff.wiki(), end="\n\n")

    def extrapolation(self):
        """差分宇宙周期演算"""
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> extrapolation` required"
        for challenge in self.__game.rogue_tourn_weekly_challenge():
            print(challenge.wiki(), end="\n\n")

    def book(self, title: str | None = None, pretty: bool = False, cure: bool = False):
        """书籍"""
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> book` required"
        if cure:
            for item in self.__game.item_cure_info_data():
                if title is not None and item.title != title:
                    continue
                if pretty:
                    print(self.__formatter.format(item.desc), end="\n\n")
                else:
                    print(item.wiki(), end="\n\n")
            return
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

    def text(self, *hashes: int | str):
        match self.__game:
            case gsz.sr.GameData():
                for hash in hashes:
                    assert isinstance(hash, int), "SR TextMap only allow int"
                hashes = typing.cast(tuple[int, ...], hashes)
                print("\n".join(self.__game.text(gsz.sr.excel.Text(hash=hash)) for hash in hashes))
            case gsz.zzz.GameData():
                for hash in hashes:
                    assert isinstance(hash, str), "ZZZ TextMap only allow str"
                hashes = typing.cast(tuple[str, ...], hashes)
                print("\n".join(self.__game.text(hash) for hash in hashes))
            case None:
                raise ValueError("`--base <GameData> text` required")

    def talk(self, *ids: int):
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> talk` required"
        for id in ids:
            talk = self.__game.talk_sentence_config(id)
            assert talk is not None
            print(f"{talk.name}：{talk.text}")

    def message(self, contacts_name: str | None = None, section_id: int | None = None):
        match self.__game:
            case gsz.sr.GameData():
                self.__message_sr(self.__game, contacts_name, section_id)
            case gsz.zzz.GameData():
                self.__message_zzz(self.__game)
            case None:
                raise ValueError("`--base <GameData> message` required")

    def __message_sr(self, game: gsz.sr.GameData, contacts_name: str | None = None, section_id: int | None = None):
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> message` required"
        if section_id is not None:
            assert isinstance(section_id, int)
            section = game.message_section_config(section_id)
            if section is not None:
                print(section.wiki())
            return
        if contacts_name is not None:
            assert isinstance(contacts_name, str)
        for contacts in game.message_contacts_config():
            if contacts_name is not None and self.__formatter.format(contacts.name) != contacts_name:
                continue
            print(contacts.wiki(), end="\n\n")

    def __message_zzz(self, game: gsz.zzz.GameData):
        """TODO: 完成 ZZZ BWiki 补充后改为模板"""
        assert isinstance(self.__game, gsz.zzz.GameData), "`--base <ZenlessData> message` required"
        for group in game.message_group_config():
            print(f"\n\033[1m{group.contact_name}\033[22m <!-- {group.id} -->", end="")
            quests = list(group.quests())
            if len(quests) != 0:
                print("\n  相关任务:", "、".join(quest.name for quest in quests), end="")
            print(group.wiki())

    def rogue_npc(self):
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> rogue-npc` required"
        for npc in itertools.chain(
            self.__game.rogue_npc(), self.__game.rogue_tourn_npc(), self.__game.rogue_magic_npc()
        ):
            for dialogue in npc.dialogue_list():
                print(npc.name, dialogue.dialogue_path, end=" ")
                print(dialogue.wiki(debug=True), end="\n\n")

    def challenge(
        self,
        type: typing.Literal["memory", "story", "boss"] | None = None,
        current: bool = False,
        next: bool = False,
        date: str | None = None,
    ):
        assert isinstance(self.__game, gsz.sr.GameData), "`--base <TurnBasedGameData> challenge` required"
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

    MIYOUSHE_SR_OFFICIAL = 288909600
    BILIBILI_SR_OFFICIAL = 1340190821
    BILIBILI_SR_POM_POM = 508103429
    BILIBILI_SR_WUBBABOO = 3493120220071960
    SOCIAL_MEDIA_VIDEO_KEYWORDS = [
        "动画短片",
        "千星纪游PV",
        "黄金史诗PV",
        "角色PV",
        "角色前瞻",
        "走近星穹",
        "星穹美学速递",
        "星旅一瞬",
        "版本PV",
        "前瞻特别节目",
        "EP",
        "夜间车厢",
        "虚一直构",
        "浮光映影",
        "参展视频",
        "OP",
        "PV",
    ]
    SOCIAL_MEDIA_IMAGE_KEYWORDS = ["星旅留影", "帕姆展览馆 | 光锥故事", "帕姆展览馆 | 表情包", "帕姆展览馆"]

    async def social_media(self):  # noqa: PLR0915
        TRIM_CATEGORY = re.compile(r"^[^|丨]+[\|丨]\s*")
        DIRECTORY = pathlib.Path("崩坏：星穹铁道媒体")
        await aiofiles.os.makedirs(DIRECTORY, exist_ok=True)
        async with gsz.bbs.bilibili.Client() as client:
            videos = itertools.chain(
                [video async for video in client.space(self.BILIBILI_SR_OFFICIAL).search()],
                [video async for video in client.space(self.BILIBILI_SR_POM_POM).search()],
                [video async for video in client.space(self.BILIBILI_SR_WUBBABOO).search()],
            )
        video_titles_revmap = {video.title.removeprefix("《崩坏：星穹铁道》"): video for video in videos}
        video_titles = list(video_titles_revmap.keys())
        streams = {
            keyword: io.BytesIO()
            for keyword in itertools.chain(
                self.SOCIAL_MEDIA_VIDEO_KEYWORDS,
                self.SOCIAL_MEDIA_IMAGE_KEYWORDS,
                ("未分类",),
            )
        }
        async with gsz.bbs.Client() as client:
            async for post in client.user_post_list(self.MIYOUSHE_SR_OFFICIAL):
                # subject 偶尔会多敲空格，需要把空格都去掉再比较
                subject = post.subject.strip().replace("\xa0", "").removeprefix("《崩坏：星穹铁道》")
                video_covers = [content.video_cover for content in post.structured_content()]
                if any(video_covers):  # 有视频
                    category = next(
                        (keyword for keyword in self.SOCIAL_MEDIA_VIDEO_KEYWORDS if keyword in subject), "未分类"
                    )
                    description = "".join(filter(None, (content.text for content in post.structured_content())))
                    description = description.strip().replace("\n", "<br />")
                    # 通过最长公共子序列来判断视频是否匹配
                    video_title = difflib.get_close_matches(subject, video_titles)
                    if len(video_title) == 0:
                        logging.warning("%s not found on bilibili", subject)
                    video = video_titles_revmap[video_title[0]] if len(video_title) != 0 else None
                    title = video.title if video is not None else post.subject
                    title = title.replace("|", "")
                    bvid = str(video.bvid) if video is not None else ""
                    stream = streams[category]
                    _ = stream.write("{{视频|标题=".encode())
                    _ = stream.write(title.encode())
                    _ = stream.write(f"|BV号={bvid}|简介={description}".encode())
                    _ = stream.write("|角色=}}".encode())
                    _ = stream.write(f"\n<!-- https://www.miyoushe.com/sr/article/{post.id} -->".encode())
                    if video is not None:
                        _ = stream.write(f"\n<!-- https://www.bilibili.com/video/{bvid} -->".encode())
                    _ = stream.writelines(f"\n<!-- 米封面 {cover} -->".encode() for cover in video_covers if cover)
                    if video is not None:
                        _ = stream.write(f"\n<!-- 哔封面 {video.cover} -->".encode())
                    _ = stream.write(b"\n\n")
                    continue
                category = next((keyword for keyword in self.SOCIAL_MEDIA_IMAGE_KEYWORDS if keyword in subject), None)
                if category is not None:  # 角色贺图
                    stream = streams[category]
                    _ = stream.write(f"<!-- https://www.miyoushe.com/sr/article/{post.id} -->\n".encode())
                    _ = stream.write(f"'''{TRIM_CATEGORY.sub('', subject)}'''\n".encode())
                    structured_texts = (
                        content.text.strip() for content in post.structured_content() if content.text is not None
                    )
                    _ = stream.write("<br />\n".join(structured_texts).encode())
                    for content in post.structured_content():
                        if content.image is not None:
                            _ = stream.write(f"\n[[文件:<!-- {content.image} -->|500px]]".encode())
                    _ = stream.write(b"\n\n")
        # 整合信息，判断是否和旧文件相同，如不同则备份旧文件后写入
        localtz = zoneinfo.ZoneInfo("localtime")
        for category, stream in streams.items():
            file_path = DIRECTORY / re.sub(r"\W", "", category)
            if await aiofiles.os.path.exists(file_path):
                size = await aiofiles.os.path.getsize(file_path)
                # 文件长度是单调递增的，因为媒体只会越来越多（除非崩铁删视频），所以可以用长度判断
                if len(stream.getvalue()) == size:
                    continue
                ctime = await aiofiles.os.path.getctime(file_path)
                cdate = datetime.datetime.fromtimestamp(ctime, tz=localtz).date()
                await aiofiles.os.replace(file_path, f"{file_path}-{cdate}")
            async with aiofiles.open(file_path, "wb") as file:
                _ = await file.write(stream.getvalue())

    def inter_knot(self):  # noqa: PLR0912
        """TODO: 结构化、完成 ZZZ BWiki 补充后改为模板"""
        assert isinstance(self.__game, gsz.zzz.GameData), "`--base <ZenlessData> inter-knot` required"
        for post in self.__game.inter_knot_config():
            print("#" * 80)
            print(f"\x1b[1m{post.title}\x1b[m", end=" ")
            print("<!--", post.id, end=" ")
            if post.image != "":
                print("PostImg:", post.image, end=" ")
            print("-->")
            print(textwrap.indent(post.text, "  "))
            print()
            for comment in post.comments():
                print(f"  - \x1b[1m{comment.commentator}\x1b[m:", comment.text)
            if post.replies is not None:
                if post.replies[1] == "":
                    print("  回复:", post.replies[0])
                    comments = post.follow_up()
                    if comments is None:
                        continue
                    for comment in comments[0]:
                        print(f"  - \x1b[1m{comment.commentator}\x1b[m:", comment.text)
                elif post.same_follow_up:
                    comments = post.follow_up()
                    print("  回复 1:", post.replies[0])
                    print("  回复 2:", post.replies[1])
                    if comments is None:
                        continue
                    for comment in comments[0]:
                        print(f"  - \x1b[1m{comment.commentator}\x1b[m:", comment.text)
                else:
                    comments = post.follow_up()
                    print("  回复 1:", post.replies[0])
                    if comments is not None:
                        for comment in comments[0]:
                            print(f"    - \x1b[1m{comment.commentator}\x1b[m:", comment.text)
                    print("  回复 2:", post.replies[1])
                    if comments is not None:
                        for comment in comments[1]:
                            print(f"    - \x1b[1m{comment.commentator}\x1b[m:", comment.text)

    def main(self):
        """调试代码可以放这里"""


if __name__ == "__main__":
    fire.Fire(Main)  # pyright: ignore[reportUnknownMemberType]
