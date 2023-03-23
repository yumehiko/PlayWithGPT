from modules.userCommandType import UserCommandType
from modules.loggableMessage import LoggableMessage
from modules.talker_type import TalkerType
from modules import gptContact
from modules import logReader
from modules import file_finder
from rx.subject import Subject

class UserCommands:
    def __init__(self):
        self.print_message = Subject()
        self.send_message = Subject()


    def try_run_command(self, question : str) -> UserCommandType:
        if question == "Clear" or question == "clear" or question == "c":
            gptContact.clearContext()
            self.print_message.on_next((LoggableMessage(TalkerType.command, "=== 文脈をクリアします。AIは記憶を失いますが、会話は続行できます ===")))
            return UserCommandType.CLEAR

        if question == "Log" or question == "log" or question == "l":
            self.print_message.on_next((LoggableMessage(TalkerType.command, "=== 最新のログを表示します ===", False)))
            log = logReader.ReadLatestJson()
            self.print_message.on_next((LoggableMessage(TalkerType.command, log, False)))
            self.print_message.on_next((LoggableMessage(TalkerType.command, "=== 以上が最新のログです ===", False)))
            self.print_message.on_next((LoggableMessage(TalkerType.command, "=== 最新のログを表示しました（記録上は省略） ===")))
            return UserCommandType.LOG

        if question.startswith("read: "):
            question = question[6:]
            file_name = question.split(".py")[0] + ".py"
            source_code = file_finder.findSourceCode(file_name)
            commandText = file_name + "の内容は次の通りです：\n" + source_code
            self.send_message.on_next((LoggableMessage(TalkerType.user, commandText, False)))
            self.print_message.on_next((LoggableMessage(TalkerType.command, "=== " + file_name + "のソースコードを読み上げました ===")))
            return UserCommandType.READ

        if question == "End" or question == "end" or question == "e":
            return UserCommandType.END
        
        return UserCommandType.NONE