from abc import ABC, abstractmethod
from modules.command_type import CommandType
from modules.talker import Talker
from modules.chat_message import ChatMessage
from modules.chat_controller import ChatController
from modules import log_reader
from modules import file_finder
import re

class Command(ABC):
    @abstractmethod
    def execute(self, message: ChatMessage, system_talker: Talker) -> CommandType:
        pass

    @abstractmethod
    def match(self, message_text: str) -> bool:
        pass


class ShowLatestLogCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller

    def match(self, message_text: str) -> bool:
        return message_text.lower() in ["log", "l"]

    def execute(self, message: ChatMessage, system_talker: Talker) -> CommandType:
        message = ChatMessage("=== 最新のログを表示します ===", system_talker.sender_info, False)
        self.chat_controller.print_message(message)
        log = log_reader.ReadLatestJson()
        message = ChatMessage(log, system_talker.sender_info, False)
        self.chat_controller.print_message(message)
        message = ChatMessage("=== 最新のログを表示しました（Log上では省略） ===", system_talker.sender_info)
        self.chat_controller.print_message(message)
        self.chat_controller.skip = True
        return CommandType.LOG



class ReadCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller

    def match(self, message_text: str) -> bool:
        return bool(re.match(r"^(Read:|read: ).*\.py$", message_text))

    def execute(self, message: ChatMessage, system_talker: Talker) -> CommandType:
        command = message.text[6:]
        file_name = command.split(".py")[0] + ".py"
        source_code = file_finder.findSourceCode(file_name)
        commandText = file_name + "の内容は次の通りです：\n" + source_code
        self.chat_controller.send_to_all(ChatMessage(commandText, system_talker.sender_info, False))
        message = ChatMessage("=== " + file_name + "のソースコードを読み上げました ===", system_talker.sender_info)
        self.chat_controller.print_message(message)
        self.chat_controller.skip = True
        return CommandType.READ


class ClearCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller
        
    def match(self, message_text: str) -> bool:
        return message_text.lower() in ["clear", "c"]

    def execute(self, message: ChatMessage, system_talker: Talker) -> CommandType:
        self.chat_controller.clear_context()
        self.chat_controller.skip = True
        return CommandType.CLEAR


class EndCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller
        
    def match(self, message_text: str) -> bool:
        return message_text.lower() in ["end", "e"]

    def execute(self, message: ChatMessage, system_talker: Talker) -> CommandType:
        self.chat_controller.end_session()
        self.chat_controller.skip = True
        return CommandType.END
