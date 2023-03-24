from modules.talker import Talker
from modules.chat_message import ChatMessage
from modules.talker_type import TalkerType
from modules import chatLogger
from modules.abstract_ui import AbstractUI
import colorama
import openai
import yaml
import asyncio

class ChatController:
    
    def __init__(self, view: AbstractUI) -> None:
        self.view = view

    async def one_on_one_session(self, talkerA: Talker, talkerB: Talker):
        """
        1対1の会話を開始する。
        """

        # ログを初期化する
        chatLogger.initialize()
        colorama.init()

        # Systemとして振る舞うTalkerを定義する。
        self.system = Talker(TalkerType.system, "system")

        # 設定ファイルからAPIキーを読み込み、OpenAIのAPIキーとして設定する。
        with open("key.yaml") as key_file:
            config = yaml.safe_load(key_file)
            openai.api_key = config["openai"]["api_key"]
            # APIキーが設定できたか確認し、設定されていない場合は例外を返す
            if not openai.api_key:
                raise ValueError("APIKey is not set.")

        self.main_loop = asyncio.create_task(self.session_loop(talkerA, talkerB))


    async def session_loop(self, talkerA: Talker, talkerB: Talker) -> None:
        try:
            while True:
                message = await talkerA.generate_message()
                chatLogger.log(message)
                talkerB.receive_message(message)
                message = await talkerB.generate_message()
                chatLogger.log(message)
                talkerA.receive_message(message)
        except asyncio.CancelledError:
            raise
        finally:
            self.view.print_message(ChatMessage("=== ログを記録しました。セッションを終了します ===", self.system))
            chatLogger.saveJson()


    def end_session(self) -> None:
        """
        会話を終了する。
        """
        self.main_loop.cancel()

    # メッセージにコマンドが含まれているかを判定し、boolで返す
    def is_command(self, message: str) -> bool:
        return message.startswith("/")

        """
        
        userCommands = UserCommands()
        userCommands.print_message.subscribe(self.print_loggable_message)
        userCommands.send_message.subscribe(
            lambda message: bot.receive_message("user", message.text))

        aiCommands = AICommands()
        aiCommands.print_message.subscribe(self.print_loggable_message)

        self.view.print_manual()

        while True:
            question = await self.view.request_user_input()
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
            bot.receive_message("user", question)
            response = bot.generate_message()
            loggable_response = LoggableMessage(TalkerType.assistant, response)

            # 返答を表示・記録する。
            self.print_loggable_message(loggable_response)

            # 返答がコマンドを含む場合、コマンドを実行する。
            aiCommands.try_execute_command(response)
        """