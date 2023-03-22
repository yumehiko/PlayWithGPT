import yaml
import openai

class GPTBot:

    def __init__(self, mode="", model_id="gpt-3.5-turbo"):
        """
        クラスを初期化する。APIキーを渡し、文脈を初期化する。
        """
        # 設定ファイルからAPIキーを読み込む
        with open("key.yaml") as key_file:
            config = yaml.safe_load(key_file)
            openai.api_key = config["openai"]["api_key"]
        
        # 会話の文脈を初期化する
        self.context = []

        # model_idを設定する
        self.model_id = model_id
        
        # モードを設定する
        if mode:
            self.send_system_message(mode)
    
    def send_system_message(self, message):
        """
        role: system として API にメッセージを送る
        """
        formatted_message = {"role": "system", "content": message}
        self.context.append(formatted_message)
    
    def send_user_message(self, message):
        """
        role: user として API にメッセージを送る
        """
        formatted_message = {"role": "user", "content": message}
        self.context.append(formatted_message)
    
    def request_message(self):
        """
        GPT-3 にこれまでの文脈を渡し、発言を要求し、その本文を返し、文脈を記憶する。
        """
        # APIキーが設定済みか確認し、設定されていない場合は例外を返す
        if not openai.api_key:
            raise ValueError("APIKey is not set.")
        
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=self.context,
        )
            
        # 返答を整形する。
        response_body = response.choices[0].text.strip()
        formatted_response = {"role": "assistant", "content": response_body}

        # 文脈を追記する
        self.context.append(formatted_response)

        return response_body
    
    def clear_context(self):
        """
        文脈をクリアする。
        """
        self.context = []
