from .talker import Talker
from .chat_message import ChatMessage
from .session import Session
from . import code_generator
from . import log_reader
from . import file_finder
from abc import ABC, abstractmethod
import re
import json

class Command(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        pass

    @abstractmethod
    def match(self, message_text: str) -> bool:
        pass


class ShowLatestLogCommand(Command):
    def match(self, message_text: str) -> bool:
        keywords = ["log", "l"]
        return message_text.lower() in keywords

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        message = ChatMessage("=== 最新のログを表示します ===", system_talker.sender_info, False)
        self.session.print_message(message)
        log = log_reader.ReadLatestJson()
        message = ChatMessage(log, system_talker.sender_info, False)
        self.session.print_message(message)
        message = ChatMessage("=== 最新のログを表示しました（Log上では省略） ===", system_talker.sender_info)
        self.session.print_message(message)
        self.session.skip = True


class ReadCommand(Command):
    def match(self, message_text: str) -> bool:
        return bool(re.match(r"^(Read:|read: ).*\..*$", message_text))

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        file_name = message.text[6:]
        print(file_name)
        source_code = file_finder.read_file(file_name)
        commandText = file_name + "の内容は次の通りです：\n" + source_code
        self.session.send_to_all(ChatMessage(commandText, system_talker.sender_info, False))
        message = ChatMessage("=== " + file_name + "のソースコードを読み上げました ===", system_talker.sender_info)
        self.session.print_message(message)
        self.session.skip = True


class ClearCommand(Command):
    def match(self, message_text: str) -> bool:
        keywords = ["clear", "c"]
        return message_text.lower() in keywords

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        self.session.clear_context()
        self.session.skip = True


class EndCommand(Command):
    def match(self, message_text: str) -> bool:
        keywords = ["end", "e"]
        if message_text.lower() in keywords:
            return True
        if "execute: End" in message_text:
            return True
        return False

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        self.session.end()
        self.session.skip = True
    

class GenerateModuleCommand(Command):
    def match(self, message_text: str) -> bool:
        return "execute: GenerateModule: " in message_text

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        chat_text = message.text.split("GenerateModule: ")[1]
        file_name = chat_text.split(".py")[0] + ".py"
        source_code = chat_text.split(".py")[1]

        code_generator.generate_module(file_name, source_code)
        message = ChatMessage("=== " + file_name + "を生成しました ===", system_talker.sender_info)
        self.session.print_message(message)



class GenerateTaskCommand(Command):
    def match(self, message_text: str) -> bool:
        return "execute: GenerateTask: " in message_text
    
    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        chat_text = message.text.split("GenerateTask: ")[1]
        file_name = chat_text.split(".py")[0] + ".task"
        task = chat_text.split(".py")[1]
        
        # .taskファイルとしてtasks/に書き出す
        directory = "tasks/"
        with open(directory + file_name, 'w', encoding="utf-8") as f:
            f.write(task)



class RequestModuleCommand(Command):
    def match(self, message_text: str) -> bool:
        return bool(re.match(r"^(execute: Request: ).*\..*$", message_text))

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        match = re.search(r'\b\w+\.py\b', message.text)
        if match:
            file_name = match.group(0)
        else:
            Exception("ファイル名が見つかりませんでした")
        print(file_name)
        source_code = file_finder.read_file(file_name)
        commandText = file_name + "の内容は次の通りです：\n" + source_code
        self.session.send_to_all(ChatMessage(commandText, system_talker.sender_info, False))
        message = ChatMessage("=== " + file_name + "のソースコードを読み上げました ===", system_talker.sender_info)
        self.session.print_message(message)
        self.session.skip = True


class WritePersonaCommand(Command):
    def match(self, message_text: str) -> bool:
        return "execute: WritePersona: " in message_text

    def execute(self, message: ChatMessage, system_talker: Talker) -> None:
        file_name = self.write_persona_file(message)
        message = ChatMessage("Personaファイル: " + file_name + "が生成されました。", system_talker.sender_info)
        self.session.print_message(message)

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