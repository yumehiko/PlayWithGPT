# cui.py
from modules.loggableMessage import LoggableMessage
from modules.talker_type import TalkerType
import colorama
from rx.subject import Subject
from typing import TypeVar

T = TypeVar('T')

class CUI:
    def __init__(self):
        self.on_input: Subject[str] = Subject()
        self.on_print: Subject[LoggableMessage] = Subject()

        colorama.init()

    def user_input(self):
        input_text = input("You: ")
        self.on_input.on_next(input_text)

    def print_message(self, message: LoggableMessage):
        color = colorama.Fore.WHITE
        reset = colorama.Style.RESET_ALL

        if message.talker == TalkerType.assistant:
            color = colorama.Fore.CYAN
        elif message.talker == TalkerType.command:
            color = colorama.Fore.YELLOW

        print(color + message.text + reset)
        self.on_print.on_next(message)

        # 空行を入れる
        print()