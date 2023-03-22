from userCommandType import UserCommandType
import gptContact
import chatLogger
import logReader
import findModule
import rx


class UserCommands:
    def __init__(self):
        self.userCommandType = rx.subjects.Subject()
        self.userCommandText = rx.subjects.Subject()


    def try_run_command(self, question : str) -> UserCommandType:
        if question == "Clear" or question == "clear" or question == "c":
            gptContact.clearContext()
            commandText = "=== 文脈をクリアします。AIは記憶を失いますが、会話は続行できます ==="
            chatLogger.log("command", commandText)
            self.userCommandText = commandText
            return UserCommandType.CLEAR

        if question == "Log" or question == "log" or question == "l":
            commandText = "=== 最新のログを表示します ==="
            self.userCommandText = commandText
            log = logReader.ReadLatestJson()
            self.userCommandText = log
            commandText = "=== 以上が最新のログです ==="
            self.userCommandText = commandText
            commandText = "=== 最新のログを表示しました（記録上は省略） ==="
            chatLogger.log("command", commandText)
            return UserCommandType.LOG

        if question.startswith("read: "):
            question = question[6:]
            file_name = question.split(".py")[0] + ".py"
            source_code = findModule.findSourceCode(file_name)
            commandText = file_name + "について話します。内容は、次の通りです：\n" + source_code
            gptContact.sendUserMessage(commandText)
            self.userCommandText = commandText
            chatLogger.log("command", commandText)
            return UserCommandType.READ

        if question == "End" or question == "end" or question == "e":
            commandText = "=== ログを記録しました。セッションを終了します ==="
            chatLogger.log("command", commandText)
            chatLogger.saveJson()
            self.userCommandText = commandText
            return UserCommandType.END
        
        return UserCommandType.NONE