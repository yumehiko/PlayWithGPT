from modules import gptContact
from modules import chatLogger
from modules import aiCommand
from modules import logReader
from modules import findModule


def startSession():
    """
    GPT-3との会話を開始する
    """

    # 会話ループを開始する
    chatLoop()


def chatLoop():
    """
    ユーザーが会話をする。ユーザーの入力によってコマンドがある：
        Clear、またはcと入力すると、文脈をクリア。
        Log、またはlと入力すると、最新のログを参照する（文脈には含まれない）。
        End、またはeと入力すると、ログを記録し、セッションを終了する。
    """

    while True:
        question = input("あなた: ")
        if question == "Clear" or question == "clear" or question == "c":
            gptContact.clearContext()
            commandText = "=== 文脈をクリアします。AIは記憶を失いますが、会話は続行できます ==="
            chatLogger.log("command", commandText)
            printMessage(commandText)
            continue

        if question == "Log" or question == "log" or question == "l":
            commandText = "=== 最新のログを表示します ==="
            printMessage(commandText)
            log = logReader.ReadLatestJson()
            printMessage(log)
            commandText = "=== 以上が最新のログです ==="
            printMessage(commandText)
            commandText = "=== 最新のログを表示しました（記録上は省略） ==="
            chatLogger.log("command", commandText)
            continue

        if question.startswith("read: "):
            question = question[6:]
            file_name = question.split(".py")[0] + ".py"
            source_code = findModule.findSourceCode(file_name)
            commandText = file_name + "について話します。内容は、次の通りです：\n" + source_code
            gptContact.sendUserMessage(commandText)
            printMessage(commandText)
            chatLogger.log("command", commandText)
            continue

        if question == "End" or question == "end" or question == "e":
            commandText = "=== ログを記録しました。セッションを終了します ==="
            chatLogger.log("command", commandText)
            chatLogger.saveJson()
            printMessage(commandText)
            break

        chatLogger.log("user", question)
        response = gptContact.ask(question)
        chatLogger.log("assistant", response)
        printMessage("AI: " + response)
        aiCommand.executeCommand(response)

# メッセージを表示する
def printMessage(message):
    print(message + "\n")