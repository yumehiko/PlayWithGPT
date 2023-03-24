from modules.talker_type import TalkerType
from modules.talker import Talker

"""
Chatのメッセージを表すクラス。
"""

class ChatMessage:
    def __init__(self, text: str, sender: Talker, should_log: bool = True):
        self.text = text
        self.sender = sender
        self.should_log = should_log