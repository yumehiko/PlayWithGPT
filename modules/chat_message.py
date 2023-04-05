from rx.subject import Subject # type: ignore[attr-defined]
from modules.talker_type import TalkerType



class SenderInfo:
    """
    ChatMessageの送信者情報。
    """
    def __init__(self, name: str, display_name: str, type: TalkerType):
        self.name = name
        self.display_name = display_name
        self.type = type



class ChatMessage:
    """
    Chatのメッセージを表すクラス。
    """
    def __init__(self, text: str, sender_info: SenderInfo, should_log: bool = True) -> None:
        self.text = text
        self.sender_info = sender_info
        self.should_log = should_log



class ChatMessageSubject(Subject):
    """
    内部の型をstrに限定したSubject。
    """
    def on_next(self, value: ChatMessage) -> None:
        super().on_next(value)