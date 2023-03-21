import gptContact
import chatLogger
import userInterface

# これは、このファイルが直接実行された場合にのみ実行されます。
if __name__ == "__main__":
    

    # モデルを初期化する
    gptContact.initialize()
    chatLogger.initialize()
    userInterface.startSession()
