import chatLogger
import userInterface
import moduleGenerator

# コマンドのリスト
commandList = ["generateModule: "]

# 発言がexecute: から始まる場合、コマンドリストから適合するコマンドを探し、実行する。
def executeCommand(voice):
    if not voice.startswith("execute: "):
        return
    
    voice = voice[9:]

    if voice.startswith("generateModule: "):
        file_name = moduleGenerator.write_py_file(voice[16:])
        prompt = "=== ChatGPTがモジュール：" + file_name + "を生成しました ==="
        userInterface.printMessage(prompt)
        chatLogger.log("command", prompt)
        return

    prompt = voice[:20] +"は不明なコマンドです。"
    userInterface.printMessage(prompt)
    chatLogger.log("command", prompt)