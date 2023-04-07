"""
アプリケーションの起点となるモジュール。CUIバージョン。
"""

from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.command_handler import CommandHandler
from modules.app_initializer import AppInitializer
from modules.cui import CUI
from modules import log_writer
import asyncio

class Main:
    def __init__(self) -> None:
        # system_talkerはシステムとしての発言を行うためのオブジェクト。
        self.system_talker = Talker(TalkerType.system, "System")

        # CUIモードのインターフェースを生成する。
        self.view = CUI(self.system_talker)

        log_writer.initialize()

        self.app_initializer = AppInitializer(self.view, self.system_talker)


    async def run(self) -> None:
        """
        アプリケーションのメインループ。
        """
        # アプリケーションのモードを選択する。
        try:
            session = await self.app_initializer.ask_app_mode()
        except Exception:
            raise

        # 会話コントローラおよびコマンドハンドラを生成する。
        self.command_handler = CommandHandler(self.system_talker, session)

        # 会話ロジックループを開始。
        try:
            await session.begin()
        finally:
            log_writer.saveJson()



if __name__ == "__main__":
    main = Main()
    asyncio.run(main.run())
