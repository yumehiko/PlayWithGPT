import chatLogger

# コマンドのリスト
commandList = ["apple"]

# 発言がexecute: から始まる場合、コマンドリストから適合するコマンドを探し、実行する。
def executeCommand(voice):
    if not voice.startswith("execute: "):
        return
    
    voice = voice[9:]

    if not voice in commandList:
        prompt = "コマンドが見つかりませんでした。"
        print(prompt)
        chatLogger.log(prompt)
        return
    
    if voice == "apple":
        prompt = "=== りんごパーティだ！！　うおおお！！！ ==="
        print(prompt)
        chatLogger.log("command", prompt)

# 発言を受けて、その発言がコマンドリストに含まれているかを返す。
def isCommand(voice):
    if voice in commandList:
        return True
    else:
        return False