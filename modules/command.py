from abc import ABC, abstractmethod
from modules.talker import Talker
from modules.chat_message import ChatMessage
from modules.chat_controller import ChatController
from modules import code_generator
from modules import log_reader
from modules import file_finder
import re
import json

class Command(ABC):
    @abstractmethod
    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        pass

    @abstractmethod
    def match(self, message_text: str) -> bool:
        pass


class ShowLatestLogCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller

    def match(self, message_text: str) -> bool:
        keywords = ["log", "l"]
        return message_text.lower() in keywords

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        message = ChatMessage("=== 最新のログを表示します ===", system_talker.sender_info, False)
        self.chat_controller.print_message(message)
        log = log_reader.ReadLatestJson()
        message = ChatMessage(log, system_talker.sender_info, False)
        self.chat_controller.print_message(message)
        message = ChatMessage("=== 最新のログを表示しました（Log上では省略） ===", system_talker.sender_info)
        self.chat_controller.print_message(message)
        self.chat_controller.skip = True


class ReadCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller

    def match(self, message_text: str) -> bool:
        return bool(re.match(r"^(Read:|read: ).*\..*$", message_text))

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        file_name = message.text[6:]
        print(file_name)
        source_code = file_finder.read_file(file_name)
        commandText = file_name + "の内容は次の通りです：\n" + source_code
        self.chat_controller.send_to_all(ChatMessage(commandText, system_talker.sender_info, False))
        message = ChatMessage("=== " + file_name + "のソースコードを読み上げました ===", system_talker.sender_info)
        self.chat_controller.print_message(message)
        self.chat_controller.skip = True


class ClearCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller
        
    def match(self, message_text: str) -> bool:
        keywords = ["clear", "c"]
        return message_text.lower() in keywords

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        self.chat_controller.clear_context()
        self.chat_controller.skip = True


class EndCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller
        
    def match(self, message_text: str) -> bool:
        keywords = ["end", "e"]
        return message_text.lower() in keywords

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        self.chat_controller.end_session()
        self.chat_controller.skip = True
    

class GenerateModuleCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller
    
    def match(self, message_text: str) -> bool:
        return "execute: generateModule: " in message_text

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        file_name = code_generator.write_py_file(message.text)
        message = ChatMessage("=== " + file_name + "を生成しました ===", system_talker.sender_info)
        self.chat_controller.print_message(message)


class WritePersonaCommand(Command):
    def __init__(self, chat_controller: ChatController):
        self.chat_controller = chat_controller
    
    def match(self, message_text: str) -> bool:
        return "execute: writePersona: " in message_text

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        file_name = self.write_persona_file(message)
        message = ChatMessage("Personaファイル: " + file_name + "が生成されました。", system_talker.sender_info)
        self.chat_controller.print_message(message)

    def write_persona_file(self, message: ChatMessage) -> str:
        # execute: writePersona: を除く
        persona_data = message.text
        persona_data = persona_data.replace("execute: writePersona:", "").strip()
        # 文字列をディクショナリに変換する
        data = json.loads(persona_data)
        # ファイル名を生成する
        file_name = f"{data['name'].lower().replace(' ', '')}.json"
        directory = "personas/"
        # ディクショナリをJSONファイルに書き込む
        with open(directory + file_name, "w") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=2)
        return file_name