from .command import Command
from .chat_message import ChatMessage
from .session import Session
from .command import EndCommand, ClearCommand, ReadCommand, ShowLatestLogCommand, GenerateModuleCommand, GenerateTaskCommand, RequestModuleCommand, WritePersonaCommand
from .talker import Talker
from typing import Dict

class CommandHandler:
    def __init__(self, system_talker: Talker, session: Session) -> None:
        self.system_talker = system_talker
        self.chat_controller = session
        self.commands: list[Command] = [
            EndCommand(session),
            ClearCommand(session),
            ReadCommand(session),
            ShowLatestLogCommand(session),
            GenerateModuleCommand(session),
            GenerateTaskCommand(session),
            RequestModuleCommand(session),
            WritePersonaCommand(session),
        ]
        session.message_subject.subscribe(self.handle)

    def handle(self, message: ChatMessage) -> None:
        for command in self.commands:
            if command.match(message.text):
                command.execute(message, self.system_talker)
                return
