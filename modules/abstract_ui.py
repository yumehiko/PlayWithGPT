

from abc import ABC, abstractmethod
from modules.chat_message import ChatMessage
from modules.talker import Talker


class AbstractUI(ABC):
    def __init__(self) -> None:
        self.manual = [
            "=== PlayWithGPT CUIモード ===",
            "Clear、またはcと入力すると、文脈をクリアします。",
            "Log、またはlと入力すると、最新のログを参照します（文脈には含まれない）。",
            "read: fileName.pyと入力すると、fileName.pyのソースコードをBotに対して読み上げます。",
            "End、またはeと入力すると、セッションを終了します。",
            "=== 会話を開始します ===",
        ]
    
    @abstractmethod
    def print_manual(self, system_talker: Talker) -> None:
        """
        ユーザーに対して、このアプリケーションの使い方を表示する。
        """
        pass

    @abstractmethod
    async def request_user_input(self) -> str:
        """
        ユーザーからの入力を待機し、入力された文字列を返す。
        """
        pass

    @abstractmethod
    def print_message(self, message: ChatMessage) -> None:
        """
        メッセージを表示する。
        """
        pass