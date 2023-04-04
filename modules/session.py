from modules.talker import Talker
from modules.translater import Translater, TranslateType
from modules.chat_message import ChatMessage
from enum import Enum
import yaml



class SessionType(Enum):
    none = 0
    one_on_one = 1
    bot_on_bot = 2
    cancel = 3



class Session:
    def __init__(self, participiants: list[Talker], type: SessionType, translate_type: TranslateType) -> None:
        self.participants = participiants
        self.session_mode = type
        self.translate_mode = translate_type
    

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
        with open('config.yaml', 'w', encoding="utf-8") as outfile:
            yaml.dump(self.__dict__, outfile)