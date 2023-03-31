from modules.abstract_ui import AbstractUI
from modules.talker import Talker
from modules.chat_message import ChatMessage
from modules.gptBot import GPTBot
import enum
import asyncio

class TranslateMode(enum.Enum):
    """
    翻訳モードの種類。
    """
    none = 0
    deepl = 1
    chatgpt = 2


class AppInitializer:
    """
    PlayWithGPTの初期設定を行うクラス。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker) -> None:
        self.view = view
        self.system_talker = system_talker

    async def ask_app_mode(self) -> None:
        await self.ask_translate_mode()

    async def ask_translate_mode(self) -> TranslateMode:
        text = "PlayWithGPTの起動設定を選択してください。\n"
        text += "翻訳モード：\n"
        text += "    (n) 翻訳なし\n"
        text += "    (d) DeepL翻訳\n"
        text += "    (g) ChatGPT翻訳\n"
        message = ChatMessage("PlayWithGPTの起動モードを選択してください。", self.system_talker.sender_info, False)
        self.view.print_message(message)
        input = ""
        while(input != "n" and input != "d" and input != "g"):
            try:
                input = await self.view.request_user_input()
            except asyncio.CancelledError:
                raise

        if input == "d": 
            return TranslateMode.deepl
        elif input == "g":
            return TranslateMode.chatgpt
        else:
            return TranslateMode.none
    """
    async def ask_bot_select(self) -> GPTBot:
        text = "会話したいBotの名前を入力してください"
        message = ChatMessage(text, self.system_talker.sender_info, False)
        self.view.print_message(message)
        input = ""
        while(input != "1" and input != "2"):
            try:
                input = await self.view.request_user_input()
            except asyncio.CancelledError:
                raise
    """ 