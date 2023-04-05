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


async def main_loop() -> None:
    """
    アプリケーションのメインループ。
    """

    # CUIモードのインターフェースを生成する。
    view = CUI() # type: ignore

    # system_talkerはシステムとしての発言を行うためのオブジェクト。
    system_talker = Talker(TalkerType.system, "System")

    # 会話コントローラおよびコマンドハンドラを生成する。
    controller = ChatController(view, system_talker)
    command_handler = CommandHandler(system_talker, controller)

    app_initializer = AppInitializer(view, system_talker, controller)
    session = await app_initializer.ask_app_mode()

    # 会話ロジックループを開始。
    await controller.begin_session(session)

if __name__ == "__main__":
    asyncio.run(main_loop())
