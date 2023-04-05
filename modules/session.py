from modules.talker import Talker
from modules.translater import Translater, TranslateType
from modules.chat_message import ChatMessage
from enum import Enum
import yaml
from yaml import MappingNode
from typing import Union, IO


class SessionType(Enum):
    none = 0
    one_on_one = 1
    bot_on_bot = 2
    cancel = 3



class SessionConfig:
    def __init__(self, participant_names: list[str], session_type: SessionType, translate_type: TranslateType) -> None:
        self.participant_names = participant_names
        self.session_type = session_type
        self.translate_type = translate_type



class SessionConfigLoader(yaml.SafeLoader):
    def __init__(self, stream: Union[str, bytes, IO[str], IO[bytes]]) -> None:
        super().__init__(stream)

    def read_session_config(self, node: MappingNode) -> SessionConfig:
        data = self.construct_mapping(node)
        return SessionConfig(
            participant_names=data["participants"],
            session_type=SessionType[data["session_type"]],
            translate_type=TranslateType[data["translate_type"]]
        )

    
SessionConfigLoader.add_constructor("!SessionConfig", SessionConfigLoader.read_session_config)



class Session:
    def __init__(self, participiants: list[Talker], type: SessionType, translate_type: TranslateType) -> None:
        self.participants = participiants
        self.type = type
        self.translate_type = translate_type
    

    def set_translater(self, translater: Translater) -> None:
        self.translater = translater


    def send_to(self, message: ChatMessage, target: Talker) -> None:
        """
        指定した話者にメッセージを送信する。
        """
        if target.sender_info != message.sender_info:
            target.receive_message(message)


    def send_to_all(self, message: ChatMessage) -> None:
        """
        会話に参加している全ての話者にメッセージを送信する。
        """
        for participant in self.participants:
            self.send_to(message, participant)
    

    def clear_context(self) -> None:
        """
        全員の会話のコンテキストをクリアする。
        """
        for participant in self.participants:
            participant.clear_context()


    def write_as_yaml(self) -> None:
        participant_names = []
        for participant in self.participants:
            participant_names.append(participant.persona_name)
        config = {
                "participants": participant_names,
                "session_type": self.type.name,
                "translate_type": self.translate_type.name
        }

        with open("session_config.yaml", "w", encoding="utf-8") as outfile:
                outfile.write("!SessionConfig\n")
                yaml.dump(config, outfile, allow_unicode=True, explicit_start=False, default_flow_style=None, Dumper=yaml.SafeDumper)

