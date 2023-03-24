"""
ユーザーを表すクラス。
talkerを継承し、abstract_uiクラスを利用してtalkerとして振る舞う。
"""

from modules.talker import Talker
from modules.abstract_ui import AbstractUI
from modules.talker_type import TalkerType
from modules.chat_message import ChatMessage


class User(Talker):
    def __init__(self, ui: AbstractUI):
        self._type = TalkerType.user
        self.ui = ui

    @property
    def type(self) -> TalkerType:
        return self._type

    def receive_message(self, message: ChatMessage) -> None:
        """
        この話者に対して、他の話者からの発言を受け取る。
        """
        self.ui.print_message(message)

    async def generate_message(self) -> ChatMessage:
        """
        この話者に発言を要求する。
        """
        message = await self.ui.request_user_input()
        return ChatMessage(message, self, True)