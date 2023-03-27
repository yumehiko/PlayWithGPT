from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.chat_message import ChatMessage, ChatMessageSubject
from modules import chatLogger
from modules.abstract_ui import AbstractUI
from modules.interpreter import Interpreter
import colorama
import openai
import yaml
import asyncio

class ChatController:

    def __init__(self, view: AbstractUI, system_talker:Talker) -> None:
        self.view = view
        self.system_talker = system_talker
        self.message_subject = ChatMessageSubject()
        self.skip = False
        self.end = False

    
    async def start_session(self, partticipiant: list[Talker]) -> None:
        """
        会話を開始する。
        """

        # ログを初期化する
        chatLogger.initialize()
        self.participants = partticipiant

        # 設定ファイルからAPIキーを読み込み、OpenAIのAPIキーとして設定する。
        with open("key.yaml") as key_file:
            config = yaml.safe_load(key_file)
            openai.api_key = config["openai"]["api_key"]
            # APIキーが設定できたか確認し、設定されていない場合は例外を返す
            if not openai.api_key:
                raise ValueError("APIKey is not set.")
        
        self.view.print_manual(self.system_talker)
        self.main_loop = asyncio.create_task(self.session_loop())
        try:
            await self.main_loop
        except asyncio.CancelledError:
            pass
        finally:
            self.view.print_message(ChatMessage("=== ログを記録しました。セッションを終了します ===", self.system_talker.sender_info))
            chatLogger.saveJson()
            
    async def start_session_with_interpreter(self, partticipiant: list[Talker]) -> None:

        # 翻訳者を生成する。
        interpreter = Interpreter(self.system_talker)

        # ログを初期化する
        chatLogger.initialize()
        self.participants = partticipiant

        # 設定ファイルからAPIキーを読み込み、OpenAIのAPIキーとして設定する。
        with open("key.yaml") as key_file:
            config = yaml.safe_load(key_file)
            openai.api_key = config["openai"]["api_key"]
            # APIキーが設定できたか確認し、設定されていない場合は例外を返す
            if not openai.api_key:
                raise ValueError("APIKey is not set.")
            
        self.view.print_manual(self.system_talker)
        self.main_loop = asyncio.create_task(self.session_loop_with_interpreter(interpreter))
        try:
            await self.main_loop
        except asyncio.CancelledError:
            pass
        finally:
            self.view.print_message(ChatMessage("=== ログを記録しました。セッションを終了します ===", self.system_talker.sender_info))
            chatLogger.saveJson()

    async def session_loop(self) -> None:
        while not self.end:
            try:
                await self.chat()
            except asyncio.CancelledError:
                raise

    async def session_loop_with_interpreter(self, interpreter: Interpreter) -> None:
        while not self.end:
            try:
                await self.chat_with_interpreter(interpreter)
            except asyncio.CancelledError:
                raise

    async def chat(self) -> None:
        """
        参加者全員が会話を1周行う。
        """
        for participant in self.participants:
            self.skip = False
            try:
                message = await participant.generate_message()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                self.send_to_all(message)
                self.print_message(message)
            except asyncio.CancelledError:
                raise

    async def chat_with_interpreter(self, interpreter: Interpreter) -> None:
        """
        参加者全員が会話を1周行う。
        ただし、すべての発言は翻訳者によって翻訳される。
        """
        for participant in self.participants:
            self.skip = False
            try:
                message = await participant.generate_message()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                interpreter.receive_message(message)
                interpreted_message = await interpreter.generate_message()
                self.send_to_all(interpreted_message)
                # 話者がユーザーの場合のみ、翻訳前の発言を表示する。
                if message.sender_info.type == TalkerType.user:
                    self.print_message(message)
                else:
                    self.print_message(interpreted_message)
            except asyncio.CancelledError:
                raise

    def send_to_all(self, message: ChatMessage) -> None:
        """
        会話に参加している全ての話者にメッセージを送信する。
        """
        for participant in self.participants:
            self.send_to(message, participant)

    def send_to(self, message: ChatMessage, target: Talker) -> None:
        """
        指定した話者にメッセージを送信する。
        """
        if target.sender_info != message.sender_info:
            target.receive_message(message)

    def print_message(self, message: ChatMessage) -> None:
        """
        メッセージをチャット欄に表示する。
        """
        self.view.print_message(message)

        # logすべきなら、logする。
        if message.should_log:
            chatLogger.log(message)

    def clear_context(self) -> None:
        """
        会話のコンテキストをクリアする。
        """
        for participant in self.participants:
            participant.clear_context()
        self.view.print_message(ChatMessage("=== コンテキストをクリアしました ===", self.system_talker.sender_info))

    def end_session(self) -> None:
        """
        会話を終了する。
        """
        self.main_loop.cancel()