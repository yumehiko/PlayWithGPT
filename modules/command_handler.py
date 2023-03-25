from modules.command import Command
from modules.command_type import CommandType
from modules.chat_message import ChatMessage
from modules.chat_controller import ChatController
from modules.command import EndCommand, ClearCommand, ReadCommand, ShowLatestLogCommand
from modules.talker import Talker
from typing import Dict

class CommandHandler:
    def __init__(self, system_talker: Talker, chat_controller: ChatController) -> None:
        self.commands: Dict[str, Command] = {}
        self.system_talker = system_talker
        self.register_commands(chat_controller)
        chat_controller.message_subject.subscribe(self.handle)

    def register_commands(self, chat_controller: ChatController) -> None: 
        self.register_command(EndCommand(chat_controller), "End", "end", "E", "e")
        self.register_command(ClearCommand(chat_controller), "Clear", "clear", "c")
        self.register_command(ReadCommand(chat_controller), "Read:", "read:")
        self.register_command(ShowLatestLogCommand(chat_controller), "Log", "log", "l")

    def register_command(self, command: Command, *aliases: str) -> None:
        for alias in aliases:
            self.commands[alias] = command

    def handle(self, message: ChatMessage) -> None:
        for command in self.commands.values():
            if command.match(message.text):
                command.execute(message, self.system_talker)
                return
