import gptContact
import chatLogger


def startSession():
    """
    GPT-3との会話を開始する
    """

    # プロンプトメッセージを表示する
    messages = [
        "初期化完了。",
        "Clear、またはcと入力すると、文脈をクリアします。",
        "End、またはeと入力すると、セッションを終了します。",
        "会話を開始します。",
    ]
    print("\n".join(messages))

    # 会話ループを開始する
    chatLoop()


def chatLoop():
    """
    ユーザーが会話をする。ユーザーの入力によってコマンドがある：
        Clear、またはcと入力すると、文脈をクリア。
        End、またはeと入力すると、ログを記録し、セッションを終了する。
    """

    while True:
        question = input("あなた: ")
        if question == "Clear" or question == "c":
            gptContact.clearContext()
            commandText = "=== 文脈をクリアします。AIは記憶を失いますが、会話は続行できます ==="
            chatLogger.logUserCommand(commandText)
            print(commandText)
            continue

        if question == "End" or question == "e":
            commandText = "=== ログを記録しました。セッションを終了します ==="
            chatLogger.logUserCommand(commandText)
            chatLogger.saveLog()
            print(commandText)
            break

        chatLogger.logUserInput(question)
        response = gptContact.ask(question)
        chatLogger.logAIResponse(response)
        print("AI: " + response)
