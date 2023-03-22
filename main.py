from modules import gptContact
from modules import chatLogger
from modules import userInterface
from modules.gui import gui
import tkinter as tk

# これは、このファイルが直接実行された場合にのみ実行されます。
if __name__ == "__main__":
    # モデルを初期化する
    userInterface.printMessage("Chat-GPTをPythonプログラムアシスタントモードで実行します。")
    
    gptContact.initialize("あなた（assistant）は優秀なPythonプログラムアシスタントです。また、assistantはプログラム「PlayWithGPT」と連携したAIでもあります。assistantの機能は「PlayWithGPT」によって追加されています。assistantがコードを書くときは、必ず「execute: generateModule: fileName.py」と書き、その次の行からコードの内容を書いてください。コードは必ずコードブロック「```python」で始まり「```」で終えてください。fileNameには、そのコードにふさわしいファイル名を指定してください。そうすることで、assistantはPlayWithGPTにコードを追加できます。")
    chatLogger.initialize()

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

    """ UI関係。一旦コメントアウト。
    root = tk.Tk()
    app = gui(root)
    app.mainloop()
    """
    # 会話ループを開始する
    userInterface.startSession()