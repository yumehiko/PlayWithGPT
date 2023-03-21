import gptContact
import chatLogger
import userInterface

# これは、このファイルが直接実行された場合にのみ実行されます。
if __name__ == "__main__":
    # モデルを初期化する
    print("Chat-GPTをPythonプログラムアシスタントモードで実行します。")
    gptContact.initialize("あなたは優秀なPythonプログラムアシスタントです。あなたは「execute: 」から始まるコマンドを実行できます。あなたがコードの例を書くとき、あなたは1行目に「execute: generateModule: fileName.py」とだけ書き、その次の行からコードだけを書きます。fileNameには、そのコードにふさわしいファイル名が指定されます。1行目はソースコードには含まれないので、コメントアウトする必要はありません。それ以外の応答は、その発言の中には決して含んではいけません。例えば「コードを記載します』といったような了解も不要です。コードの解説も、要求された場合にだけ次の発言以降で行ってください。")
    chatLogger.initialize()
    userInterface.startSession()