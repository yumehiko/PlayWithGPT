from modules.talker_type import TalkerType

class SenderInfo:
    """
    ChatMessageの送信者情報。
    """
    def __init__(self, name: str, type: TalkerType):
        self.name = name
        self.type = type