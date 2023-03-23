from modules.gptBot import GPTBot
from modules.userCommands import UserCommands
from modules.userCommandType import UserCommandType
from modules.loggableMessage import LoggableMessage
from modules.talker_type import TalkerType
from modules import chatLogger
from modules.aiCommands import AICommands
from modules.loggableMessage import LoggableMessage
import colorama
import openai
import yaml


def one_on_one_session(bot: GPTBot):
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
    userCommands.print_message.subscribe(printMessage)
    userCommands.send_message.subscribe(
        lambda message: send_message_to(message, bot))

    aiCommands = AICommands()
    aiCommands.print_message.subscribe(printMessage)

    # ユーザーマニュアルを表示する
    manual = [
        "=== PlayWithGPT CUIモード ===",
        "Clear、またはcと入力すると、文脈をクリアします。",
        "Log、またはlと入力すると、最新のログを参照します（文脈には含まれない）。",
        "read: fileName.pyと入力すると、fileName.pyのソースコードをBotに対して読み上げます。",
        "End、またはeと入力すると、セッションを終了します。",
        "=== 会話を開始します ===",
    ]
    printMessage(LoggableMessage(TalkerType.command, "\n".join(manual)))

    while True:
        question = input("You: ")
        # 空行を入れる
        print()
        commandType = userCommands.try_run_command(question)
        # 終了コマンドが入力された場合、終了する。
        if commandType == UserCommandType.END:
            break
        # その他のコマンドが入力された場合、ユーザーの入力待機へ戻る。
        if commandType != UserCommandType.NONE:
            continue

        # コマンド入力がなかった場合、通常の会話として処理を進める。
        chatLogger.log(LoggableMessage(TalkerType.user, question))
        bot.send_message_by("user", question)

        # GPTからの返答を受け取る。
        response = bot.request_response()
        printMessage(LoggableMessage(TalkerType.assistant, response))
        aiCommands.try_execute_command(response)

    printMessage(LoggableMessage(TalkerType.command, "=== ログを記録しました。セッションを終了します ==="))
    chatLogger.saveJson()


def printMessage(message: LoggableMessage):
    """
    指定されたメッセージを出力する。
    """

    color = colorama.Fore.WHITE
    reset = colorama.Style.RESET_ALL
    if (message.talker == TalkerType.assistant):
        color = colorama.Fore.CYAN
    elif (message.talker == TalkerType.command):
        color = colorama.Fore.YELLOW

    print(color + message.text + reset)
    # ログに残す場合、ログに残す。
    if message.should_log:
        chatLogger.log(message)
    # 空行を入れる
    print()


def send_message_to(message: LoggableMessage, bot: GPTBot):
    """
    指定されたメッセージをGPTBotに送信する。
    """

    bot.send_message_by("user", message.text)
