import json
from datetime import datetime

logData = []

def initialize():
    """
    ログデータを初期化する
    """
    logData.clear()


def logUserInput(question):
    """
    ユーザーのテキスト入力を受けて、整形したjson形式の情報をlogDataに追加する
    """
    # 発言日時を取得
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # 発言内容を整形
    formatted_question = {"role": "user", "content": question, "datetime": now}
    # logDataに追加
    logData.append(formatted_question)


def logAIResponse(response):
    """
    アシスタントの発言を受けて、整形したjson形式の情報をlogDataに追加する
    """
    # 発言日時を取得
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # 発言内容を整形
    formatted_response = {"role": "assistant", "content": response, "datetime": now}
    # logDataに追加
    logData.append(formatted_response)


def logUserCommand(command):
    """
    ユーザーのコマンドを受けて、整形したjson形式の情報をlogDataに追加する
    """
    # 発言日時を取得
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # 発言内容を整形
    formatted_command = {"role": "command", "content": command, "datetime": now}
    # logDataに追加
    logData.append(formatted_command)


def saveLog():
    """
    ログデータをjson形式で保存する
    """
    # ファイル名を取得
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "log/" + now + ".json"
    # ログデータをjson形式で保存
    with open(filename, "w") as f:
        json.dump(logData, f, indent=4, ensure_ascii=False)