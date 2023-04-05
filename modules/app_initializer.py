from modules.abstract_ui import AbstractUI
from modules.talker import Talker
from modules.chat_message import ChatMessage
from modules.user import User
from modules.gptBot import GPTBot
from modules.chat_controller import ChatController
from modules.session import Session, SessionConfig, SessionType, SessionConfigLoader
from modules.translater import Translater, GptTranslater, DeepLTranslater, TranslateType
import openai
import yaml
from enum import Enum
import os
import asyncio



class AppInitializer:
    """
    PlayWithGPTの初期設定を行うクラス。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker, chat_controller: ChatController) -> None:
        self.view = view
        self.system_talker = system_talker
        self.chat_controller = chat_controller

        # 設定ファイルからAPIキーを読み込み、OpenAIのAPIキーとして設定する。
        with open("key.yaml") as key_file:
            config = yaml.safe_load(key_file)
            openai.api_key = config["openai"]["api_key"]
            # APIキーが設定できたか確認し、設定されていない場合は例外を返す
            if not openai.api_key:
                raise ValueError("APIKey is not set.")
            self.deepl_api_key = config["deepl"]["api_key"]


    async def ask_app_mode(self) -> Session:
        # session_config.yamlがあるかどうかを確認し、あるならそれを読み込む。
        if await self.ask_load_last_session_config():
            session = self.read_session_config_by_yaml()
            if session.translate_type != TranslateType.none:
                translater = self.pick_translater(session.translate_type)
                session.set_translater(translater)
            return session
        
        session_type = await self.ask_session_type()
        participient: list[Talker] = []
        translate_type = TranslateType.none
        if session_type == SessionType.cancel:
            raise Exception("No Session")
        elif session_type == SessionType.one_on_one:
            translate_type = await self.ask_translate_mode()
            user = User(self.view)
            bot = await self.ask_bot_select()
            participient = [user, bot]
        elif session_type == SessionType.bot_on_bot:
            translate_type = await self.ask_translate_mode()
            bot1 = await self.ask_bot_select()
            bot2 = await self.ask_bot_select()
            participient = [bot1, bot2]
        
        session = Session(participient, session_type, translate_type)

        if translate_type != TranslateType.none:
            translater = self.pick_translater(translate_type)
            session.set_translater(translater)

        return session
    
    async def ask_load_last_session_config(self) -> bool:
        """
        session_configの設定を読み込むか尋ねる。
        """

        # session_config.yamlがない場合はFalseを返す。
        if not os.path.exists("session_config.yaml"):
            return False

        text = "前回のセッション設定で始めますか？（y/n）"
        self.view.print_message(ChatMessage(text, self.system_talker.sender_info, False))
        while True:
            answer = await self.view.request_user_input()
            if answer == "y":
                return True
            elif answer == "n":
                return False
            else:
                self.view.print_message(ChatMessage("yかnを入力してください。", self.system_talker.sender_info, False))
            
    def read_session_config_by_yaml(self) -> Session:
        """
        session_config.yamlから設定を読み込む。
        """
        with open("session_config.yaml", "r", encoding="utf-8") as infile:
            session_config: SessionConfig = yaml.load(infile, Loader = SessionConfigLoader)
            participants: list[Talker] = []
            for participant_name in session_config.participant_names:
                talker: Talker
                if participant_name == "user":
                    talker = User(self.view)
                else:
                    talker = GPTBot(participant_name, self.system_talker)
                participants.append(talker)
            session = Session(participants, session_config.session_type, session_config.translate_type)
            return session

    async def ask_session_type(self) -> SessionType:
        text = "セッションタイプを選択してください：\n"
        text += "    (o) ユーザーとBotのOne-on-Oneセッション\n"
        text += "    (b) Bot同士のオートセッション\n"
        text += "    (c) キャンセル\n"
        message = ChatMessage(text, self.system_talker.sender_info, False)
        self.view.print_message(message)
        input = ""
        while(input != "o" and input != "b" and input != "c"):
            try:
                input = await self.view.request_user_input()
            except asyncio.CancelledError:
                raise
        if input == "o":
            message = ChatMessage("One-on-Oneセッションを開始します。", self.system_talker.sender_info, False)
            self.view.print_message(message)
            return SessionType.one_on_one
        elif input == "b":
            message = ChatMessage("Bot同士のオートセッションを開始します。", self.system_talker.sender_info, False)
            self.view.print_message(message)
            return SessionType.bot_on_bot
        else:
            return SessionType.cancel
        

    async def ask_bot_select(self) -> GPTBot:
        text = "会話したいBotの名前を入力してください"
        message = ChatMessage(text, self.system_talker.sender_info, False)
        self.view.print_message(message)
        directory = "personas/"
        persona_name = ""
        bot_confirm: bool = False
        while(not bot_confirm):
            try:
                persona_name = await self.view.request_user_input()
                file_name = persona_name + ".json"
                filepath = os.path.join(directory, file_name)
                bot_confirm = os.path.exists(filepath)
            except asyncio.CancelledError:
                raise
        bot = GPTBot(persona_name, self.system_talker)
        return bot
    

    async def ask_translate_mode(self) -> TranslateType:
        text = "翻訳モードを選択してください：\n"
        text += "    (n) 翻訳なし\n"
        text += "    (d) DeepL翻訳\n"
        text += "    (g) ChatGPT翻訳\n"
        message = ChatMessage(text, self.system_talker.sender_info, False)
        self.view.print_message(message)
        input = ""
        while(input != "n" and input != "d" and input != "g"):
            try:
                input = await self.view.request_user_input()
            except asyncio.CancelledError:
                raise

        if input == "d": 
            message = ChatMessage("DeepL翻訳を選択しました。", self.system_talker.sender_info, False)
            self.view.print_message(message)
            return TranslateType.deepl
        elif input == "g":
            message = ChatMessage("ChatGPT翻訳を選択しました。", self.system_talker.sender_info, False)
            self.view.print_message(message)
            return TranslateType.chatgpt
        else:
            message = ChatMessage("翻訳なしを選択しました。", self.system_talker.sender_info, False)
            self.view.print_message(message)
            return TranslateType.none
    

    def pick_translater(self, translate_mode: TranslateType) -> Translater:
        if translate_mode == TranslateType.deepl and self.deepl_api_key:
            return DeepLTranslater(self.deepl_api_key)
        elif translate_mode == TranslateType.deepl and not self.deepl_api_key:
            message = ChatMessage("DeepL APIキーが設定されていません。ChatGPT翻訳で実行します。", self.system_talker.sender_info, False)
            self.view.print_message(message)
            return GptTranslater(self.system_talker)
        elif translate_mode == TranslateType.chatgpt:
            return GptTranslater(self.system_talker)
        else:
            raise ValueError("未定義の翻訳者")