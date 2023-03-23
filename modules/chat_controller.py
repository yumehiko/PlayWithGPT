from modules.gptBot import GPTBot
from modules.userCommands import UserCommands
from modules.userCommandType import UserCommandType
from modules.loggableMessage import LoggableMessage
from modules.talker_type import TalkerType
from modules import chatLogger
from modules.aiCommands import AICommands
from modules.abstract_ui import AbstractUI
import colorama
import openai
import yaml

class ChatController:
    
    def __init__(self, view: AbstractUI) -> None:
        self.view = view

    def one_on_one_session(self, bot: GPTBot):
        """
        1対1の会話を開始する。
        """

        # ログを初期化する
        chatLogger.initialize()
        colorama.init()

        # 設定ファイルからAPIキーを読み込み、OpenAIのAPIキーとして設定する。
        with open("key.yaml") as key_file:
            config = yaml.safe_load(key_file)
            openai.api_key = config["openai"]["api_key"]
            # APIキーが設定できたか確認し、設定されていない場合は例外を返す
            if not openai.api_key:
                raise ValueError("APIKey is not set.")

        userCommands = UserCommands()
        userCommands.print_message.subscribe(self.print_loggable_message)
        userCommands.send_message.subscribe(
            lambda message: bot.send_message_by("user", message.text))

        aiCommands = AICommands()
        aiCommands.print_message.subscribe(self.print_loggable_message)

        self.view.print_manual()
        
        while True:
            question = self.view.user_input()
            commandType = userCommands.try_run_command(question)
            # 終了コマンドが入力された場合、終了する。
            if commandType == UserCommandType.END:
                break
            # その他のコマンドが入力された場合、ユーザーの入力待機へ戻る。
            if commandType != UserCommandType.NONE:
                continue

            # コマンド入力がなかった場合、通常の会話として記録し、処理を進める。
            self.print_loggable_message(LoggableMessage(TalkerType.user, question))
            
            # GPTにメッセージを送り、返答を受け取る。
            bot.send_message_by("user", question)
            response = bot.request_response()
            loggable_response = LoggableMessage(TalkerType.assistant, response)

            # 返答を表示・記録する。
            self.print_loggable_message(loggable_response)

            # 返答がコマンドを含む場合、コマンドを実行する。
            aiCommands.try_execute_command(response)

        self.view.print_message(LoggableMessage(TalkerType.command, "=== ログを記録しました。セッションを終了します ==="))
        chatLogger.saveJson()
    

    def print_loggable_message(self, message: LoggableMessage):
        """
        メッセージを表示し、必要なら記録に残す。
        """
        self.view.print_message(message)
        chatLogger.log(message)