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

class Main:
    def __init__(self) -> None:
        """
        アプリケーションの初期化を行う。
        """
        # system_talkerはシステムとしての発言を行うためのオブジェクト。
        self.system_talker = Talker(TalkerType.system, "System")

        # GUIモードのインターフェースを生成する。
        self.view = GUI(self.system_talker)

        # ロジック部を初期化する。
        self.controller = ChatController(self.view, self.system_talker)
        self.command_handler = CommandHandler(self.system_talker, self.controller)
        self.app_initializer = AppInitializer(self.view, self.system_talker, self.controller)
        self.view.main_window.show()

    async def run(self) -> None:
        """
        アプリケーションのメインループ。
        """
        # アプリケーションのモードを選択する。
        try:
            session = await self.app_initializer.ask_app_mode()
        except Exception:
            raise

        # 会話ロジックループを開始。
        await self.controller.begin_session(session)

if __name__ == "__main__":
    main = Main()

    # Qtイベントループとasyncioイベントループを一緒に実行
    loop = qasync.QEventLoop(main.view.get_app_instance())
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main.run())
    finally:
        loop.close()