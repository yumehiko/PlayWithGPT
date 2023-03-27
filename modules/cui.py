from modules.chat_message import ChatMessage
from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.abstract_ui import AbstractUI
from aioconsole import ainput
import colorama


class CUI(AbstractUI):
    def __init__(self) -> None:
        super().__init__()
        colorama.init()

    def print_manual(self, system_talker: Talker) -> None:
        """
        ユーザーに対して、このアプリケーションの使い方を表示する。
        """
        self.print_message(ChatMessage("\n".join(self.manual), system_talker.sender_info, False))

    async def request_user_input(self) -> str:
        """
        ユーザーからの入力を待機し、入力された文字列を返す。
        """
        input_text: str = await ainput("You: ")
        return input_text

    def print_message(self, message: ChatMessage) -> None:
        """
        メッセージを表示する。
        """
        
        # CUIでは、ユーザーの出力は表示済みなので、その場合空行だけ入れて無視する。
        if message.sender_info.type == TalkerType.user:
            print()
            return

        color = colorama.Fore.WHITE
        reset = colorama.Style.RESET_ALL
        talker_mark = ""

        if message.sender_info.type == TalkerType.assistant:
            color = colorama.Fore.YELLOW
        elif message.sender_info.type == TalkerType.system:
            color = colorama.Fore.CYAN

        if message.sender_info.type == TalkerType.assistant:
            talker_mark = "Bot: "

        print(color + talker_mark + message.text + reset)

        # 空行を入れる
        print()