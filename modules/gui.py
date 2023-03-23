from modules.abstract_ui import AbstractUI
from modules.loggableMessage import LoggableMessage
from modules.talker_type import TalkerType
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
from concurrent.futures import Future
import sys

class GUI(AbstractUI):
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self.window)
        self.text_edit.setReadOnly(True)
        self.line_edit = QLineEdit(self.window)
        self.line_edit.returnPressed.connect(self.on_return_pressed)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.line_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.window.setCentralWidget(central_widget)
        self.window.setWindowTitle("PlayWithGPT GUIモード")
        self.window.show()

    def on_return_pressed(self):
        input_text = self.line_edit.text()
        self.line_edit.clear()
        self.user_input_callback(input_text)

    def run(self):
        sys.exit(self.app.exec_())

    def print_manual(self):
        manual = [
            "=== PlayWithGPT GUIモード ===",
            "Clear、またはcと入力すると、文脈をクリアします。",
            "Log、またはlと入力すると、最新のログを参照します（文脈には含まれない）。",
            "read: fileName.pyと入力すると、fileName.pyのソースコードをBotに対して読み上げます。",
            "End、またはeと入力すると、セッションを終了します。",
            "=== 会話を開始します ===",
        ]

        self.print_message(LoggableMessage(TalkerType.command, "\n".join(manual)))

    def request_user_input(self) -> str:
        self.user_input_callback = None
        self.user_input_future: Future[str] = Future()

        def callback(input_text):
            if self.user_input_callback:
                self.user_input_callback = None
                self.user_input_future.set_result(input_text)

        self.user_input_callback = callback
        return self.user_input_future.result()

    def print_message(self, message: LoggableMessage) -> None:
        talker = ""

        if message.talker == TalkerType.user:
            talker = "You: "
        elif message.talker == TalkerType.assistant:
            talker = "Bot: "

        self.text_edit.append(f"{talker}{message.text}\n")