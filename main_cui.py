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
            await self.wait_for_user_input()


    async def wait_for_user_input(self) -> None:
        """
        ユーザーが何らかの入力をするまで待ち、その後アプリケーションを終了する。
        """
        text = "=== セッションが完了しました ===\n"
        text += "=== 何か入力すると、終了します ==="
        self.view.print_message_as_system(text, False)
        self.view.enable_user_input()
        await self.view.request_user_input()


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.run())
