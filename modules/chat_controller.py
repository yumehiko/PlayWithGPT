from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.chat_message import ChatMessage, ChatMessageSubject
from modules import chatLogger
from modules.abstract_ui import AbstractUI
from modules.translater import Translater, GptTranslater, DeepLTranslater
from modules.translate_mode import TranslateMode
import asyncio

# TODO: モードの組み合わせを実現する
# Interpreter_Mode: None, GPT-3.5-Turbo, DeepL
# Persona: string

class Session:
    def __init__(self, participiants: list[Talker], translate_mode: TranslateMode) -> None:
        self.participants = participiants
        self.translate_mode = translate_mode
    

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



class ChatController:
    def __init__(self, view: AbstractUI, system_talker:Talker) -> None:
        self.view = view
        self.system_talker = system_talker
        self.message_subject = ChatMessageSubject()
        self.skip = False
        self.end = False

    async def begin_session(self, session: Session) -> None:
        """
        会話を開始する。
        """
        self.session = session
        chatLogger.initialize()
        self.view.print_manual(self.system_talker)
        if(session.translate_mode != TranslateMode.none):
            self.main_loop = asyncio.create_task(self.session_loop_with_translater(session))
        else:
            self.main_loop = asyncio.create_task(self.session_loop(session))
        
        try:
            await self.main_loop
        except asyncio.CancelledError:
            pass
        finally:
            self.view.print_message(ChatMessage("=== ログを記録しました。セッションを終了します ===", self.system_talker.sender_info))
            chatLogger.saveJson()


    async def session_loop(self, session: Session) -> None:
        while not self.end:
            try:
                await self.chat(session)
            except asyncio.CancelledError:
                raise


    async def session_loop_with_translater(self, session: Session) -> None:
        while not self.end:
            try:
                await self.chat_with_translater(session)
            except asyncio.CancelledError:
                raise


    async def chat(self, session: Session) -> None:
        """
        参加者全員が会話を1周行う。
        """
        for participant in session.participants:
            self.skip = False
            try:
                message = await participant.generate_message()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                session.send_to_all(message)
                self.print_message(message)
            except asyncio.CancelledError:
                raise


    async def chat_with_translater(self, session: Session) -> None:
        """
        参加者全員が会話を1周行う。
        ただし、すべての発言は翻訳者によって翻訳される。
        """
        for participant in session.participants:
            self.skip = False
            try:
                message = await participant.generate_message()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                translated_message = await session.translater.translate(message)
                session.send_to_all(translated_message)
                # 話者がユーザーの場合のみ、翻訳前の発言を表示する。
                if message.sender_info.type == TalkerType.user:
                    self.print_message(message)
                else:
                    self.print_message(translated_message)
            except asyncio.CancelledError:
                raise


    def print_message(self, message: ChatMessage) -> None:
        """
        メッセージをチャット欄に表示する。
        """
        self.view.print_message(message)

        # logすべきなら、logする。
        if message.should_log:
            chatLogger.log(message)

    def send_to_all(self, message: ChatMessage) -> None:
        self.session.send_to_all(message)

    def clear_context(self) -> None:
        """
        全員の会話のコンテキストをクリアする。
        """
        self.session.clear_context()
        self.view.print_message(ChatMessage("=== コンテキストをクリアしました ===", self.system_talker.sender_info))


    def end_session(self) -> None:
        """
        会話を終了する。
        """
        self.main_loop.cancel()