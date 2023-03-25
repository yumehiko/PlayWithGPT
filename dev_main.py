"""
アプリケーションの起点となるモジュール。その開発版です。
"""

from modules.user import User
from modules.gptBot import GPTBot
from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.command_handler import CommandHandler
from modules.cui import CUI
from modules.chat_controller import ChatController
import asyncio


async def main_loop() -> None:
    """
    アプリケーションのメインループ。
    """

    # CUIモードのインターフェースを生成する。
    view = CUI()

    # system_talkerはシステムとしての発言を行うためのオブジェクト。
    system_talker = Talker(TalkerType.system, "System")

    # userはユーザーとしての会話を行うためのオブジェクト。
    user = User(view)


    # 会話コントローラおよびコマンドハンドラを生成する。
    controller = ChatController(view, system_talker)
    command_handler = CommandHandler(system_talker, controller)

    participants: list[Talker] = [user]
    # CUIモードの会話ループを開始する。
    await controller.start_session(participants)




if __name__ == "__main__":
    asyncio.run(main_loop())
