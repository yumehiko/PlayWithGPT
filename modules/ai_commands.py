from modules import code_generator
from modules.chat_message import ChatMessage
from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.chat_message import ChatMessage, ChatMessageSubject

class AICommands:
    def __init__(self) -> None:
        self.print_message = ChatMessageSubject()

    # 発言がexecute: から始まる場合、コマンドリストから適合するコマンドを探し、実行する。
    def try_execute_command(self, voice: str, system_talker: Talker) -> None:
        if not "execute: " in voice:
            return
        
        voice = voice.split("execute: ")[1]

        # モジュール生成コマンド
        if voice.startswith("generateModule: "):
            file_name = code_generator.write_py_file(voice[16:])
            prompt = "=== ChatGPTがモジュール：" + file_name + "を生成しました ==="
            self.print_message.on_next(ChatMessage(prompt, system_talker.sender_info))
            return
        
        prompt = "=== エラー：" + voice[:20] +"は不明なコマンドです ==="
        self.print_message.on_next(ChatMessage(prompt, system_talker.sender_info))