from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.chat_message import ChatMessage
from typing import List, Dict
import requests
import openai
import json
from abc import ABC, abstractmethod
from enum import Enum



class TranslateType(Enum):
    """
    翻訳モードの種類。
    """
    none = 0
    deepl = 1
    chatgpt = 2



class Translater(ABC):
    """
    翻訳者の基底クラス。
    """
    @abstractmethod
    async def translate(self, message: ChatMessage) -> ChatMessage:
        """
        与えられたテキストを翻訳して返す。
        """
        pass



class GptTranslater(Translater):
    """
    ChatGPTによる翻訳
    """

    def __init__(self, system_talker: Talker) -> None:
        self.system_talker = system_talker
        # personaを読み込み、botのmodel_id、name、personalityを設定する。
        with open("personas/" + "translater" + ".json", encoding="utf-8") as persona_file:
            persona = json.load(persona_file)
            self.persona_name = persona["persona_name"]
            self.display_name = persona["display_name"]
            self._talker_type = TalkerType.assistant
            self.model_id = persona["model_id"]
            self.personality = persona["personality"]

        self.personality_memory = {
            "role": system_talker.sender_info.type.name, "content": self.personality}

    async def translate(self, message: ChatMessage) -> ChatMessage:
        print("原文：", message.text)

        if message.sender_info.type == TalkerType.assistant:
            command = "次の文章を日本語に翻訳しなさい："
        else:
            command = "次の文章を英語に翻訳しなさい："

        command_message = {"role": self.system_talker.type.name, "content": command}
        formatted_message = {"role": message.sender_info.type.name, "content": message.text}

        response_data = openai.ChatCompletion.create(  # type: ignore[no-untyped-call]
            model=self.model_id,
            # personality_memoryとmemoried_messageをmessagesに追加する。
            messages=[self.personality_memory, command_message, formatted_message],
        )

        # 返答を整形する。
        response = response_data["choices"][0]["message"]["content"]
        return ChatMessage(response, message.sender_info, True)


class DeepLTranslater(Translater):
    """
    DeepLによる翻訳
    """
    def __init__(self, api_key: str) -> None:
        self.API_KEY = api_key

    async def translate(self, message: ChatMessage) -> ChatMessage:
        print("原文：", message.text)
        if message.sender_info.type == TalkerType.assistant:
            source_lang = 'EN'
            target_lang = 'JA'
        else :
            source_lang = 'JA'
            target_lang = 'EN'

        # パラメータの指定
        params = {
            'auth_key': self.API_KEY,
            'text': message.text,
            'source_lang': source_lang,  # 翻訳対象の言語
            "target_lang": target_lang  # 翻訳後の言語
        }

        # リクエストを投げる
        request = requests.post("https://api-free.deepl.com/v2/translate", data=params)

        # レスポンスを解析して翻訳されたテキストを取得
        translated_text = request.json()["translations"][0]["text"]
        translated_message = ChatMessage(
            translated_text, message.sender_info, message.should_log)
        return translated_message
