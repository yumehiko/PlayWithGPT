from modules import chatLogger
from modules import userInterface
from modules import gptBot

# これは、このファイルが直接実行された場合にのみ実行されます。
if __name__ == "__main__":
    # モデルを初期化する
    userInterface.printMessage("Chat-GPTをPythonプログラムアシスタントモードで実行します。")
    
    # GPTBotをインスタンス化する
    # managerを設定。
    with open("roleplay_settings/manager.txt", "r", encoding="utf-8") as txt_file:
        manager_settings = txt_file.read()
    manager = gptBot.GPTBot(mode=manager_settings)

    # coderを設定。
    with open("roleplay_settings/coder.txt", "r", encoding="utf-8") as txt_file:
        coder_settings = txt_file.read()
    coder = gptBot.GPTBot(mode=coder_settings, model_id="code-davinci-002")

    chatLogger.initialize()
    userInterface.startSession()

    # プロンプトメッセージを表示する
    messages = [
        "初期化完了。",
        "Clear、またはcと入力すると、文脈をクリアします。",
        "Log、またはlと入力すると、最新のログを参照します（文脈には含まれない）。",
        "read: fileName.pyと入力すると、fileName.pyのソースコードを読み上げます。",
        "End、またはeと入力すると、セッションを終了します。",
        "会話を開始します。",
    ]
    userInterface.printMessage("\n".join(messages))