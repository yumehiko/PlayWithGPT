from modules.talker_type import TalkerType

"""
PrintMessageクラスは、話者、本文、ログに残すかどうかのフラグを持つ。
"""

class LoggableMessage:
    def __init__(self, talker: TalkerType, text: str, should_log: bool = True):
        self.talker = talker
        self.text = text
        self.should_log = should_log