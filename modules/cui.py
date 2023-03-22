from modules import gptContact
from modules  import chatLogger
from modules  import aiCommand

# TODO: gptContactを使わなく

def one_on_one_session():
    """
    1対1の会話をする。
    """
    question = input("あなた: ")
    chatLogger.log("user", question)
    response = gptContact.ask(question)
    chatLogger.log("assistant", response)
    printMessage("AI: " + response)
    aiCommand.executeCommand(response)

# メッセージを表示する
def printMessage(message):
    print(message)
    print("")