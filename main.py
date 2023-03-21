import gptContact
import chatLogger
import userInterface

# これは、このファイルが直接実行された場合にのみ実行されます。
if __name__ == "__main__":
    # モデルを初期化する
    print("Chat-GPTをプログラムアシスタントモードで実行します。")
    gptContact.initialize("あなたは優秀なプログラムアシスタントです。あなたは「execute: 」から始まるコマンドを実行できます。ユーザーが「appleコマンドを実行して」と発言した場合、あなたは「execute: apple」とだけ発言します。それ以外には何も発言しません。")
    chatLogger.initialize()
    userInterface.startSession()
