from modules.command_type import CommandType
from modules.chat_message import ChatMessage
from modules.talker_type import TalkerType
from modules.talker import Talker
from modules import gptContact
from modules import logReader
from modules import file_finder
from rx.subject import Subject

class UserCommands:
    def __init__(self, system: Talker):
        self.print_message = Subject()
        self.send_message = Subject()
        self.system = system


    def try_run_command_by_message(self, message : ChatMessage) -> CommandType:
        if self.is_match(message, ["Clear", "clear", "c"]):
            gptContact.clearContext()
            self.print_message.on_next((ChatMessage("=== 文脈をクリアします。AIは記憶を失いますが、会話は続行できます ===", self.system)))
            return CommandType.CLEAR


        if self.is_match(message, ["Log", "log", "l"]):
            self.print_message.on_next((ChatMessage("=== 最新のログを表示します ===", self.system, False)))
            log = logReader.ReadLatestJson()
            self.print_message.on_next((ChatMessage(log, self.system, False)))
            self.print_message.on_next((ChatMessage("=== 以上が最新のログです ===", self.system, False)))
            self.print_message.on_next((ChatMessage("=== 最新のログを表示しました（記録上は省略） ===", self.system)))
            return CommandType.LOG

        if self.is_startwith(message, ["Read: ", "read: "]):
            command = message.text[6:]
            file_name = command.split(".py")[0] + ".py"
            source_code = file_finder.findSourceCode(file_name)
            commandText = file_name + "の内容は次の通りです：\n" + source_code
            self.send_message.on_next((ChatMessage(commandText, self.system, False)))
            self.print_message.on_next((ChatMessage("=== " + file_name + "のソースコードを読み上げました ===", self.system)))
            return CommandType.READ

        if message == "End" or message == "end" or message == "e":
            return CommandType.END
        
        return CommandType.NONE
    
    # ChatMessageが指定されたlabelsのいずれかと一致するかどうかを判定する
    def is_match(self, message : ChatMessage, labels : list[str]) -> bool:
        for label in labels:
            if message.text == label:
                return True
        return False
    
    def is_startwith(self, message: ChatMessage, labels: list[str]) -> bool:
        for label in labels:
            if message.text.startswith(label):
                return True
        return False