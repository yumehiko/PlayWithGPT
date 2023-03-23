import openai
import json

class GPTBot:
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
        
        # 会話の文脈を初期化する
        self.context = []

        # personalityを文脈に追加する
        self.send_message_by("system", self.personality)


    def send_message_by(self, role, message):
        formatted_message = {"role": role, "content": message}
        self.context.append(formatted_message)
    

    def request_response(self):
        """
        GPT-3 にこれまでの文脈を渡し、発言を要求し、その本文を返し、文脈を記憶する。
        """

        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=self.context,
        )
            
        # 返答を整形する。
        response_body = response["choices"][0]["message"]["content"]
        formatted_response = {"role": "assistant", "content": response_body}

        # 文脈を追記する
        self.context.append(formatted_response)

        return response_body
    
    def clear_context(self):
        """
        文脈をクリアする。
        """
        self.context = []
