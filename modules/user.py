from modules.talker import Talker
from modules.abstract_ui import AbstractUI
from modules.talker_type import TalkerType
from modules.chat_message import ChatMessage


class User(Talker):
    """
    ユーザーを表すクラス。
    talkerを継承し、abstract_uiクラスを利用してtalkerとして振る舞う。
    """
    def __init__(self, ui: AbstractUI):
        super().__init__(TalkerType.user, "user", "User")
        self.ui = ui

    @property
    def type(self) -> TalkerType:
        return self._type

    def receive_message(self, message: ChatMessage) -> None:
        """
        この話者に対して、他の話者からの発言を受け取る。
        """
        pass

    async def generate_message(self) -> ChatMessage:
        """
        この話者に発言を要求する。
        """
        self.ui.hide_waiting_animation()
        self.ui.enable_user_input()
        text = await self.ui.request_user_input()
        message = ChatMessage(text, self.sender_info, True)
        self.ui.disable_user_input()
        self.ui.show_waiting_animation()
        return message