from modules.talker_type import TalkerType
from modules.talker import Talker
from modules.chat_message import ChatMessage
from typing import List, Dict
import openai
import json

class GPTBot(Talker):
    """
    会話の相手となるChatGPT-Bot。
    """
    def __init__(self, persona_name: str, system_talker: Talker) -> None:
        """
        persona_nameは、このBotの人格を表すjsonファイルの名前。
        """
        
        #personaを読み込み、botのmodel_id、name、personalityを設定する。
        with open("personas/" + persona_name + ".json", encoding="utf-8") as persona_file:
            persona = json.load(persona_file)
            self.model_id = persona["model_id"]
            self.personality = persona["personality"]
            super().__init__(TalkerType.assistant, persona["name"])
        
        # 会話の文脈を初期化する
        self.context: List[Dict[str, str]] = []

        self.receive_message(ChatMessage(self.personality, system_talker.sender_info, False))


    def receive_message(self, message:ChatMessage) -> None:
        """
        Botの文脈に追記する。
        """
        memorable_message = {"role": message.sender_info.type.name, "content": message.text}
        self.context.append(memorable_message)
    

    async def generate_message(self) -> ChatMessage:
        """
        これまでの文脈を元に発言を要求し、その本文を返し、自身の発言を記憶する。
        """

        response_data = openai.ChatCompletion.create(  # type: ignore[no-untyped-call]
            model=self.model_id,
            messages=self.context,
        )
            
        # 返答を整形する。
        response = response_data["choices"][0]["message"]["content"]
        memorable_response = {"role": "assistant", "content": response}

        # 文脈を追記する
        self.context.append(memorable_response)

        self.message_subject.on_next(response)
        return ChatMessage(response, self.sender_info, True)
    
    def clear_context(self) -> None:
        """
        文脈をクリアする。
        """
        self.context = []
