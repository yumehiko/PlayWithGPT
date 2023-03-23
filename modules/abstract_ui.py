

from abc import ABC, abstractmethod
from modules.loggableMessage import LoggableMessage


class AbstractUI(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def print_manual(self):
        """
        ユーザーに対して、このアプリケーションの使い方を表示する。
        """
        pass

    @abstractmethod
    def request_user_input(self) -> str:
        """
        ユーザーからの入力を待機し、入力された文字列を返す。
        """
        pass

    @abstractmethod
    def print_message(self, message: LoggableMessage) -> None:
        """
        メッセージを表示する。
        """
        pass