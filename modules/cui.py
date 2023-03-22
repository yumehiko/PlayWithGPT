from gptBot import GPTBot
from modules  import chatLogger
from modules  import aiCommand
from userCommands import UserCommands
from userCommandType import UserCommandType
import rx

def one_on_one_session(bot: GPTBot):
    """
    1対1の会話を開始する。
    """
    assistant = bot 
    userCommands = UserCommands()
    userCommands.commandText.subscribe(lambda x: printMessage(x))

    while True:
        question = input("You: ")
        commandType = userCommands.checkCommand(question)
        if commandType == UserCommandType.END:
            break
        if commandType != UserCommandType.NONE:
            continue
        chatLogger.log("user", question)
        assistant.send_message_by("user", question)
        response = assistant.request_response()
        chatLogger.log("assistant", response)
        printMessage("AI: " + response)
        aiCommand.executeCommand(response)

# メッセージを表示する
def printMessage(message):
    print(message)
    print("")