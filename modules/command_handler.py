from modules.command import Command
from modules.chat_message import ChatMessage
from modules.chat_controller import ChatController
from modules.command import *
from modules.talker import Talker
from typing import Dict

class CommandHandler:
    def __init__(self, system_talker: Talker, chat_controller: ChatController) -> None:
        self.system_talker = system_talker
        self.chat_controller = chat_controller
        self.commands: list[Command] = [
            EndCommand(chat_controller),
            ClearCommand(chat_controller),
            ReadCommand(chat_controller),
            ShowLatestLogCommand(chat_controller),
            GenerateModuleCommand(chat_controller),
            RequestModuleCommand(chat_controller),
            WritePersonaCommand(chat_controller),
        ]
        chat_controller.message_subject.subscribe(self.handle)

    def handle(self, message: ChatMessage) -> None:
        for command in self.commands:
            if command.match(message.text):
                command.execute(message, self.system_talker)
                return
