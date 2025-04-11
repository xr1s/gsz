import enum
import typing

import pydantic
import typing_extensions

from .base import ModelID, Text


class HeartDialTalk(ModelID):
    id_: int
    voice_id: int | None = None
    sdf_text: typing.Annotated[Text, pydantic.Field(alias="SDFText")]
    floor_id_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class TalkSentenceConfig(ModelID):
    talk_sentence_id: int = 0
    talk_sentence_text: Text | None = None
    textmap_talk_sentence_name: Text | None = None
    voice_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.talk_sentence_id


class VoiceType(enum.Enum):
    Archive = "Archive"
    BroadcastFar = "BroadcastFar"
    BroadcastNear = "BroadcastNear"
    BroadcastNormal = "BroadcastNormal"
    BroadcastUltraFar3 = "BroadcastUltraFar3"
    Cutscene = "Cutscene"
    MissionTalk_3d = "MissionTalk_3d"
    NPC_Far = "NPC_Far"
    NPC_Far_NoDuck = "NPC_Far_NoDuck"
    NPC_Near = "NPC_Near"
    NPC_Near_NoDuck = "NPC_Near_NoDuck"
    NPC_Normal = "NPC_Normal"
    NPC_Normal_NoDuck = "NPC_Normal_NoDuck"
    StoryNew = "StoryNew"
    SystemReverb1 = "SystemReverb1"


class VoiceConfig(ModelID):
    voice_id: int
    is_player_involved: bool = False
    voice_path: str
    voice_type: VoiceType | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.voice_id
