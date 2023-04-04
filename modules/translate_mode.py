from enum import Enum

class TranslateMode(Enum):
    """
    翻訳モードの種類。
    """
    none = 0
    deepl = 1
    chatgpt = 2