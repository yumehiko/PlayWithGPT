"""
アプリケーションの起点となるモジュール。
"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QEventLoop
import qasync
import sys
from modules.user import User
from modules.gptBot import GPTBot
from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.command_handler import CommandHandler
from modules.gui import GUI
from modules.chat_controller import ChatController
import asyncio


async def main_loop() -> None:
    """
    アプリケーションのメインループ。
    """

    # GUIモードのインターフェースを生成する。
    view = GUI()

    # system_talkerはシステムとしての発言を行うためのオブジェクト。
    system_talker = Talker(TalkerType.system, "System")

    # userはユーザーとしての会話を行うためのオブジェクト。
    user = User(view)

    # botを生成する。
    bot = GPTBot("assistant", system_talker)

    # 会話コントローラおよびコマンドハンドラを生成する。
    controller = ChatController(view, system_talker)
    command_handler = CommandHandler(system_talker, controller)

    view.run()

    participants: list[Talker] = [user, bot]
    # 会話ロジックループを開始。
    await controller.start_session(participants)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Qtイベントループとasyncioイベントループを一緒に実行
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main_loop())
    finally:
        loop.close()