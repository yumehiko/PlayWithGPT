"""
アプリケーションの起点となるモジュール。
"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QEventLoop
import qasync
from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.command_handler import CommandHandler
from modules.gui import GUI
from modules.app_initializer import AppInitializer
from modules.chat_controller import ChatController
import asyncio

async def main_loop() -> None:
    """
    アプリケーションのメインループ。
    """

    # system_talkerはシステムとしての発言を行うためのオブジェクト。
    system_talker = Talker(TalkerType.system, "System")

    controller = ChatController(view, system_talker)
    command_handler = CommandHandler(system_talker, controller)

    view.main_window.show()

    app_initializer = AppInitializer(view, system_talker, controller)
    try:
        session = await app_initializer.ask_app_mode()
    except Exception:
        raise

    # 会話ロジックループを開始。
    await controller.begin_session(session)

if __name__ == "__main__":
    # GUIモードのインターフェースを生成する。
    view = GUI()

    # Qtイベントループとasyncioイベントループを一緒に実行
    loop = qasync.QEventLoop(view.get_app_instance())
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main_loop())
    finally:
        loop.close()