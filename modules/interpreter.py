from modules.talker_type import TalkerType
from modules.talker import Talker
from modules.chat_message import ChatMessage
from typing import List, Dict
import openai
import json

class Interpreter(Talker):
    """
    通訳のみを行うBot。
    """
    def __init__(self, system_talker: Talker) -> None:
        """
        persona_nameは、このBotの人格を表すjsonファイルの名前。
        """
        
        #personaを読み込み、botのmodel_id、name、personalityを設定する。
        with open("personas/" + "interpreter" + ".json", encoding="utf-8") as persona_file:
            persona = json.load(persona_file)
            self.model_id = persona["model_id"]
            self.personality = persona["personality"]
            super().__init__(TalkerType.assistant, persona["name"])
        
        self.personality_memory = {"role": system_talker.sender_info.type.name, "content": self.personality}


    def receive_message(self, message:ChatMessage) -> None:
        """
        発言を記憶する（記憶は1発言のみ）
        """
        self.last_message = message
        print(message.text)
    

    async def generate_message(self) -> ChatMessage:
        """
        最後に記憶された発言を翻訳し、その翻訳文を返す。
        """

        memoried_message = {"role": self.last_message.sender_info.type.name, "content": self.last_message.text}

        response_data = openai.ChatCompletion.create(  # type: ignore[no-untyped-call]
            model=self.model_id,
            # pweaonliry_memoryとmemoried_messageをmessagesに追加する。
            messages = [self.personality_memory, memoried_message],
        )
            
        # 返答を整形する。
        response = response_data["choices"][0]["message"]["content"]
        return ChatMessage(response, self.last_message.sender_info, True)
