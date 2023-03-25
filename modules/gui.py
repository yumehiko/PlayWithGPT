from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QWidget
from PyQt6.QtCore import Qt
from modules.abstract_ui import AbstractUI
from modules.chat_message import ChatMessage
from modules.talker import Talker
from modules.talker_type import TalkerType
from typing import Callable
import sys
import asyncio


class GUI(AbstractUI):
    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.user_input_queue: asyncio.Queue[str] = asyncio.Queue()
        
        def on_return_pressed() -> None:
            if not self.input_line.text():
                return
            text = self.input_line.text()
            self.input_line.clear()
            asyncio.create_task(self.user_input_queue.put(text))

        self.on_return_pressed = on_return_pressed

        self.init_ui()

    def init_ui(self) -> None:
        # メインウィンドウの設定
        self.main_window.setWindowTitle("PlayWithGPT GUI Mode")
        self.main_window.resize(800, 600)

        # レイアウトとウィジェットの設定
        central_widget = QWidget(self.main_window)
        layout = QVBoxLayout(central_widget)
        self.main_window.setCentralWidget(central_widget)

        self.message_area = QTextEdit(central_widget)
        self.message_area.setReadOnly(True)
        layout.addWidget(self.message_area)

        self.input_line = QLineEdit(central_widget)
        self.input_line.setPlaceholderText("Type your message here...")
        layout.addWidget(self.input_line)

        self.input_line.returnPressed.connect(self.on_return_pressed)

    def print_manual(self, system_talker: Talker) -> None:
        self.print_message(ChatMessage("\n".join(self.manual), system_talker.sender_info, False))

    async def request_user_input(self) -> str:
        return await self.user_input_queue.get()

    def print_message(self, message: ChatMessage) -> None:
        if message.sender_info.type == TalkerType.user:
            name = "You: "
        elif message.sender_info.type == TalkerType.assistant:
            name = "Bot: "
        else:
            name = "System: "

        self.message_area.append(name + message.text)

    def run(self) -> int:
        self.main_window.show()
        return self.app.exec()
