from __future__ import annotations
from .chat_message import ChatMessage, ChatMessageSubject, SenderInfo
from .talker_type import TalkerType


class Talker():
    """
    Chatの話者の基底クラス。発言を受ける。発言を行う。
    """
    def __init__(self, talker_type: TalkerType = TalkerType.none, persona_name: str = "", display_name: str = "") -> None:
        self._text_subject = ChatMessageSubject()
        self._type = talker_type
        self.persona_name = persona_name
        self.display_name = display_name
        self._sender_info = SenderInfo(self.persona_name, self.display_name, self._type)

    @property
    def type(self) -> TalkerType:
        return self._type

    @property
    def message_subject(self) -> ChatMessageSubject:
        return self._text_subject
    
    @property
    def sender_info(self) -> SenderInfo:
        return self._sender_info

    def receive_message(self, message: ChatMessage) -> None:
        """
        この話者に対して、他の話者からの発言を受け取る。
        """
        pass

    async def generate_message(self) -> ChatMessage:
        """
        この話者に発言を要求する。
        """
        return ChatMessage("", self.sender_info, False)
    
    def clear_context(self) -> None:
        """
        会話の文脈を初期化する。
        """
        pass
