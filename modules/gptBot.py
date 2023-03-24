from modules.talker_type import TalkerType
from modules.talker import Talker
from modules.chat_message import ChatMessage
import openai
import json

class GPTBot(Talker):
    """
    会話の相手となるChatGPT-Bot。
    """
    def __init__(self, persona_name=""):
        """
        persona_nameは、このBotの人格を表すjsonファイルの名前。
        """
        
        #personaを読み込み、botのmodel_id、name、personalityを設定する。
        with open("personas/" + persona_name + ".json", encoding="utf-8") as persona_file:
            persona = json.load(persona_file)
            self.model_id = persona["model_id"]
            self.name = persona["name"]
            self.personality = persona["personality"]
            self.type = TalkerType.assistant
        
        # 会話の文脈を初期化する
        self.context = []

        # personalityを文脈に追加する
        self.receive_message("system", self.personality)


    def receive_message(self, message:ChatMessage) -> None:
        """
        Botの文脈に追記する。
        """
        memorable_message = {"role": message.sender.type.name, "content": message.text}
        self.context.append(memorable_message)
    

    async def generate_message(self) -> ChatMessage:
        """
        これまでの文脈を元に発言を要求し、その本文を返し、自身の発言を記憶する。
        """

        response_data = openai.ChatCompletion.create(
            model=self.model_id,
            messages=self.context,
        )
            
        # 返答を整形する。
        response = response_data["choices"][0]["message"]["content"]
        memorable_response = {"role": "assistant", "content": response}

        # 文脈を追記する
        self.context.append(memorable_response)

        return ChatMessage(response, self, True)
    
    def clear_context(self):
        """
        文脈をクリアする。
        """
        self.context = []
