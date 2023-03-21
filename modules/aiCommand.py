from modules import chatLogger
from modules import userInterface
from modules import moduleGenerator
from modules import findModule
from modules import gptContact

# 発言がexecute: から始まる場合、コマンドリストから適合するコマンドを探し、実行する。
def executeCommand(voice):
    if not "execute: " in voice:
        return
    
    voice = voice.split("execute: ")[1]

    # モジュール生成コマンド
    if voice.startswith("generateModule: "):
        file_name = moduleGenerator.write_py_file(voice[16:])
        prompt = "=== ChatGPTがモジュール：" + file_name + "を生成しました ==="
        userInterface.printMessage(prompt)
        chatLogger.log("command", prompt)
        return
    
    prompt = voice[:20] +"は不明なコマンドです。"
    userInterface.printMessage(prompt)
    chatLogger.log("command", prompt)