from .session import Session, SessionType
from .translater import Translater, TranslateType, Language
from .abstract_ui import AbstractUI
from .chat_message import ChatMessage
from .talker import Talker
import asyncio


class BotOnBotSession(Session):
    """
    Bot同士の会話を行う。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker, participants: list[Talker], translate_type: TranslateType) -> None:
        super().__init__(view, system_talker, participants, SessionType.bot_on_bot, translate_type)
 

    async def begin(self) -> None:
        # はじめに、ユーザーから議題の入力を受け取り、それをbot全員に送信する。
        self.view.print_message(ChatMessage("=== 議題を入力してください ===", self.system_talker.sender_info, False))
        topic = await self.view.request_user_input()
        topic = "議題：\n" + topic
        topic_message = ChatMessage(topic, self.system_talker.sender_info)
        self.send_to_all(topic_message)
        self.view.print_message(topic_message)
        return await super().begin()

    async def chat(self) -> None:
        """
        参加者全員が会話を1周行う。
        """
        for participant in self.participants:
            self.skip = False
            try:
                self.view.process_event()
                message = await participant.generate_message()
                self.view.process_event()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                if self.has_translater:
                    printable_message = await self.translater.translate(message, Language.JP)
                    self.view.process_event()
                self.send_to_all(message)
                self.print_message(printable_message)

                # botが発言するたびに、ユーザーからの入力を5秒待ち、もし入力があった場合、セッションを終了する。
                # 入力がなかった場合、セッションを続行する。
                # TODO: set_place_holder()を実装する。
                # TODO: ユーザーからの入力を受け取ると、セッションを終了する。
            except asyncio.CancelledError:
                raise