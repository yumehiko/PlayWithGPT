from modules import gptContact
from modules import chatLogger
from modules import userInterface

# これは、このファイルが直接実行された場合にのみ実行されます。
if __name__ == "__main__":
    # モデルを初期化する
    userInterface.printMessage("Chat-GPTをPythonプログラムアシスタントモードで実行します。")
    
    gptContact.initialize("あなたは優秀なPythonプログラムアシスタントです。あなたがコードを書くときは、発言の1行目に必ず「execute: generateModule: fileName.py」とだけ書き、その次の行からコードの内容を書いてください。fileNameには、そのコードにふさわしいファイル名を指定してください。不要なときに、このコマンドを発言しないでください。")
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