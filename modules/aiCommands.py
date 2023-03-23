from modules import code_generator
from modules.loggableMessage import LoggableMessage
from modules.talker_type import TalkerType
from rx.subject import BehaviorSubject

class AICommands:
    def __init__(self):
        self.print_message = BehaviorSubject(LoggableMessage(TalkerType.none, "", False))

    # 発言がexecute: から始まる場合、コマンドリストから適合するコマンドを探し、実行する。
    def try_execute_command(self, voice):
        if not "execute: " in voice:
            return
        
        voice = voice.split("execute: ")[1]

        # モジュール生成コマンド
        if voice.startswith("generateModule: "):
            file_name = code_generator.write_py_file(voice[16:])
            prompt = "=== ChatGPTがモジュール：" + file_name + "を生成しました ==="
            self.print_message.on_next((LoggableMessage(TalkerType.command, prompt)))
            return
        
        prompt = "=== エラー：" + voice[:20] +"は不明なコマンドです ==="
        self.print_message.on_next((LoggableMessage(TalkerType.command, prompt)))