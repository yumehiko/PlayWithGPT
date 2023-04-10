from .chat_message import ChatMessage
from .talker import Talker
from abc import ABC, abstractmethod

class AbstractUI(ABC):
    def __init__(self, system_talker: Talker) -> None:
        self.system_talker = system_talker


    @abstractmethod
    async def request_user_input(self) -> str:
        """
        ユーザーからの入力を待機し、入力された文字列を返す。
        """
        pass


    @abstractmethod
    def print_message(self, message: ChatMessage) -> None:
        """
        チャットメッセージを表示する。
        """
        pass


    def print_message_as_system(self, text: str, should_log: bool = True) -> ChatMessage:
        message = ChatMessage(text, self.system_talker.sender_info, should_log)
        self.print_message(message)
        return message

    @abstractmethod
    def enable_user_input(self) -> None:
        pass

    @abstractmethod
    def disable_user_input(self) -> None:
        pass


    @abstractmethod
    def show_waiting_animation(self) -> None:
        pass

    @abstractmethod
    def hide_waiting_animation(self) -> None:
        pass

    @abstractmethod
    def process_event(self) -> None:
        pass