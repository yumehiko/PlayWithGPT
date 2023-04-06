"""
アプリケーションの起点となるモジュール。CUIバージョン。
"""

from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.command_handler import CommandHandler
from modules.app_initializer import AppInitializer
from modules.cui import CUI
from modules.chat_controller import ChatController
import asyncio

class Main:
    def __init__(self) -> None:
        # system_talkerはシステムとしての発言を行うためのオブジェクト。
        self.system_talker = Talker(TalkerType.system, "System")

        # CUIモードのインターフェースを生成する。
        self.view = CUI(self.system_talker)

        # 会話コントローラおよびコマンドハンドラを生成する。
        self.controller = ChatController(self.view, self.system_talker)
        self.command_handler = CommandHandler(self.system_talker, self.controller)

        self.app_initializer = AppInitializer(self.view, self.system_talker, self.controller)


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
    asyncio.run(main.run())
