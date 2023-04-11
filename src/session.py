from .talker import Talker
from .talker_type import TalkerType
from .translater import Translater, TranslateType, NoTranslater
from .chat_message import ChatMessage, ChatMessageSubject
from .translater import TranslateType, Language
from .abstract_ui import AbstractUI
from . import log_writer
from abc import ABC, abstractmethod
from enum import Enum
import yaml
from yaml import MappingNode
from typing import Union, IO
import asyncio


class SessionType(Enum):
    none = 0
    cancel = 1
    one_on_one = 2
    bot_on_bot = 3
    auto_task = 4



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


class Session(ABC):
    def __init__(self, view: AbstractUI, system_talker: Talker, participants: list[Talker], type: SessionType, translate_type: TranslateType) -> None:
        self.view = view
        self.system_talker = system_talker
        self.participants = participants
        self.type = type
        self.translate_type = translate_type
        self.message_subject = ChatMessageSubject()
        self.is_end: bool = False
        self.skip: bool = False
        self.translater: Translater = NoTranslater()
    
    @property
    def has_translater(self) -> bool:
        """
        translaterがNoTranslaterでないかどうかを返す。
        """
        return not isinstance(self.translater, NoTranslater)


    def set_translater(self, translater: Translater) -> None:
        self.translater = translater


    async def begin(self) -> None:
        """
        会話を開始する。
        """
        manuals = [
            "=== PlayWithGPT ===",
            "Clear、またはcと入力すると、文脈をクリアします。",
            "Log、またはlと入力すると、最新のログを参照します（文脈には含まれない）。",
            "read: fileName.pyと入力すると、fileName.pyのソースコードをBotに対して読み上げます。",
            "End、またはeと入力すると、セッションを終了します。",
            "=== 会話を開始します ===",
        ]
        manual_text = "\n".join(manuals)
        self.view.print_message_as_system(manual_text, False)
        self.main_loop = asyncio.create_task(self.session_loop())
        
        try:
            await self.main_loop
        except asyncio.CancelledError:
            pass
        finally:
            self.write_as_yaml()
            self.view.print_message(ChatMessage("=== セッションを終了します ===", self.system_talker.sender_info))


    def send_to(self, message: ChatMessage, target: Talker) -> None:
        """
        指定した話者にメッセージを送信する。
        """
        if target.sender_info == message.sender_info:
            return
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
        self.view.print_message(ChatMessage("=== コンテキストをクリアしました ===", self.system_talker.sender_info))


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
    

    async def session_loop(self) -> None:
        while not self.is_end:
            try:
                await self.chat()
            except asyncio.CancelledError:
                raise

    @abstractmethod
    async def chat(self) -> None:
        """
        会話処理。
        """
        pass


    def print_message(self, message: ChatMessage) -> None:
        """
        メッセージをチャット欄に表示する。
        """
        self.view.print_message(message)

        # logすべきなら、logする。
        if message.should_log:
            log_writer.log(message)


    def end(self) -> None:
        """
        会話を終了する。
        """
        self.main_loop.cancel()