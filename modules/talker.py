"""
Chatの話者の基底クラス。発言を受ける。発言を行う。
"""

from __future__ import annotations
from modules.chat_message import ChatMessage
from modules.talker_type import TalkerType

class Talker():

    def __init__(self, type: TalkerType = TalkerType.none, persona_name: str = "") -> None:
        self._type = type
        self.name = persona_name

    @property
    def type(self) -> TalkerType:
        return self._type

    def receive_message(self, message: ChatMessage) -> None:
        """
        この話者に対して、他の話者からの発言を受け取る。
        """
        pass

    async def generate_message(self) -> ChatMessage:
        """
        この話者に発言を要求する。
        """
        return ChatMessage("", self, False)
