from .session import Session, SessionType
from .talker import Talker
from .talker_type import TalkerType
from .translater import TranslateType, Language
from .abstract_ui import AbstractUI
import asyncio


class OneOnOneSession(Session):
    """
    ユーザーとBotの1対1の会話を行う。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker, participants: list[Talker], translate_type: TranslateType) -> None:
        super().__init__(view, system_talker, participants, SessionType.one_on_one, translate_type)
    

    async def chat(self) -> None:
        """
        参加者全員が会話を1周行う。
        """
        for participant in self.participants:
            self.skip = False
            try:
                self.view.process_event()
                message = await participant.generate_message()
                printable_message = message
                self.view.process_event()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                if self.has_translater:
                    sender_is_user: bool = message.sender_info.type == TalkerType.user
                    if sender_is_user: # ユーザーからの発話なら、Botへの伝達メッセージは日本語から英語に翻訳する。
                        message = await self.translater.translate(message, Language.EN)
                    else: # Botからの発話なら、表示用のメッセージを英語から日本語に翻訳する。
                        printable_message = await self.translater.translate(message, Language.JP)
                    self.view.process_event()
                self.send_to_all(message)
                self.print_message(printable_message)
            except asyncio.CancelledError:
                raise