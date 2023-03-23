# cui.py
from modules.loggableMessage import LoggableMessage
from modules.talker_type import TalkerType
from modules.abstract_ui import AbstractUI
import colorama
import sys


class CUI(AbstractUI):
    def __init__(self):
        colorama.init()

    def print_manual(self):
        # ユーザーマニュアルを表示する
        manual = [
            "=== PlayWithGPT CUIモード ===",
            "Clear、またはcと入力すると、文脈をクリアします。",
            "Log、またはlと入力すると、最新のログを参照します（文脈には含まれない）。",
            "read: fileName.pyと入力すると、fileName.pyのソースコードをBotに対して読み上げます。",
            "End、またはeと入力すると、セッションを終了します。",
            "=== 会話を開始します ===",
        ]

        self.print_message(LoggableMessage(TalkerType.command, "\n".join(manual)))

    def user_input(self) -> str:
        # ユーザーの入力を待つ。
        input_text = input("You: ")

        # ユーザーの入力を、CUI上から消す
        input_length = len(input_text.encode("utf-8"))
        self.move_cursor_to_init_position(input_length)
        return input_text

    def print_message(self, message: LoggableMessage) -> None:
        color = colorama.Fore.WHITE
        reset = colorama.Style.RESET_ALL
        talker = ""

        if message.talker == TalkerType.assistant:
            color = colorama.Fore.YELLOW
        elif message.talker == TalkerType.command:
            color = colorama.Fore.CYAN

        if message.talker == TalkerType.user:
            talker = "You: "
        elif message.talker == TalkerType.assistant:
            talker = "Bot: "

        print(color + talker + message.text + reset)

        # 空行を入れる
        print()


    def move_cursor_to_init_position(self, length: int) -> None:
        sys.stdout.write("\033[1A\033[{}D".format(length))
        sys.stdout.flush()