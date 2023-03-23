"""
アプリケーションの起点となるモジュール。その開発版です。
"""

from modules.gptBot import GPTBot
from modules import cui

if __name__ == "__main__":
    # ボットを初期化する
    assistant = GPTBot("assistant")

    # CUIモードの会話ループを開始する
    cui.one_on_one_session(assistant)
