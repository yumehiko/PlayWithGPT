"""
アプリケーションの起点となるモジュール。その開発版です。
"""

from modules.gptBot import GPTBot
from modules.gui import GUI
from modules.chat_controller import ChatController

if __name__ == "__main__":
    # ボットを初期化する
    assistant = GPTBot("assistant")
    view = GUI()
    controller = ChatController(view)

    # CUIモードの会話ループを開始する。
    controller.one_on_one_session(assistant)
