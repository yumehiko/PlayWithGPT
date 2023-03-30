from modules.talker_type import TalkerType
from modules.talker import Talker
from modules.chat_message import ChatMessage
from typing import List, Dict
import openai
import json
from abc import ABC, abstractmethod

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
    ChatGPTによる通訳
    """
    def __init__(self, system_talker: Talker) -> None:
        #personaを読み込み、botのmodel_id、name、personalityを設定する。
        with open("personas/" + "translater" + ".json", encoding="utf-8") as persona_file:
            persona = json.load(persona_file)
            self.name = persona["name"]
            self._talker_type = TalkerType.assistant
            self.model_id = persona["model_id"]
            self.personality = persona["personality"]
        
        self.personality_memory = {"role": system_talker.sender_info.type.name, "content": self.personality}

    async def translate(self, message: ChatMessage) -> ChatMessage:
        formatted_message = {"role": message.sender_info.type.name, "content": message.text}

        response_data = openai.ChatCompletion.create(  # type: ignore[no-untyped-call]
            model=self.model_id,
            # personality_memoryとmemoried_messageをmessagesに追加する。
            messages = [self.personality_memory, formatted_message],
        )

        # 返答を整形する。
        response = response_data["choices"][0]["message"]["content"]
        return ChatMessage(response, message.sender_info, True)