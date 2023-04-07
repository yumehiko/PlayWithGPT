from modules.command import Command
from modules.chat_message import ChatMessage
from modules.session import Session
from modules.command import *
from modules.talker import Talker
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
