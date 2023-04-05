from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.chat_message import ChatMessage
from typing import List, Dict
import openai
import json

class GPTBot(Talker):
    """
    会話の相手となるChatGPT-Bot。人格を持ち、文脈を記憶し、発言する。
    """
    def __init__(self, persona_name: str, system_talker: Talker) -> None:
        """
        persona_nameは、このBotの人格を表すjsonファイルの名前。
        """
        self.system_talker = system_talker
        #personaを読み込み、botのmodel_id、name、personalityを設定する。
        with open("personas/" + persona_name + ".json", encoding="utf-8") as persona_file:
            persona = json.load(persona_file)
            self.model_id = persona["model_id"]
            self.personality = {"role": system_talker.type.name, "content": persona["personality"]}
            self.token_limit = int(persona["token_limit"])
            super().__init__(TalkerType.assistant, persona["persona_name"], persona["display_name"])
        
        # 会話の文脈を初期化する
        self.context: List[Dict[str, str]] = []
        self.context.append(self.personality)


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

        # Token数が規定数以上になった場合は、これまでの文脈を要約して圧縮する。
        total_tokens = int(response_data["usage"]["total_tokens"])
        if(total_tokens > self.token_limit):
            self.compress_to_summary()

        self.message_subject.on_next(response)
        return ChatMessage(response, self.sender_info, True)
    
    def compress_to_summary(self) -> None:
        
        system_command = {"role": "system", "content": "Command: Summarize the context so far in 400 words or less."}
        self.context.append(system_command)

        summary_data = openai.ChatCompletion.create(  # type: ignore[no-untyped-call]
            model=self.model_id,
            messages=self.context,
        )
        
        # 要約を整形する。
        summary = summary_data["choices"][0]["message"]["content"]
        memorable_response = {"role": "assistant", "content": summary}

        # 文脈をクリアし、要約を追記する
        self.clear_context()
        self.context.append(memorable_response)
        print("要約化しました。")


    def clear_context(self) -> None:
        """
        文脈をクリアする。
        """
        self.context = []
        self.context.append(self.personality)
