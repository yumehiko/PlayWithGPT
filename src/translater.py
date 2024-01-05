from .talker import Talker
from .talker_type import TalkerType
from .chat_message import ChatMessage
from typing import List, Dict
import requests
import openai
import json
from abc import ABC, abstractmethod
from enum import Enum

class Language(Enum):
    """
    翻訳先の言語。
    """
    none = 0
    EN = 1
    JP = 2



class TranslateType(Enum):
    """
    翻訳モードの種類。
    """
    undefined = 0
    none = 1
    deepl = 2
    deepl_free = 3
    chatgpt = 4



class Translater(ABC):
    """
    翻訳者の基底クラス。
    """
    @abstractmethod
    async def translate(self, message: ChatMessage, language: Language) -> ChatMessage:
        """
        与えられたテキストを翻訳して返す。
        """
        pass



class NoTranslater(Translater):
    """
    翻訳なし。
    """

    async def translate(self, message: ChatMessage, language: Language) -> ChatMessage:
        return message



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

    async def translate(self, message: ChatMessage, language: Language) -> ChatMessage:
        print("原文：", message.text)

        if language == Language.JP:
            command = "Translate the following sentences into Japanese: "
        elif language == Language.EN:
            command = "次の文章を英語に翻訳しなさい："
        else:
            raise ValueError("未定義の言語")

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


class DeepLFreeTranslater(Translater):
    """
    DeepL Free版による翻訳
    """
    def __init__(self, api_key: str) -> None:
        self.API_KEY = api_key

    async def translate(self, message: ChatMessage, language: Language) -> ChatMessage:
        print("原文：", message.text)
        if language == Language.JP:
            source_lang = 'EN'
            target_lang = 'JA'
        elif language == Language.EN:
            source_lang = 'JA'
            target_lang = 'EN'
        else:
            raise ValueError("未定義の言語")

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
