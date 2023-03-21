import json
from datetime import datetime

logData = []

def initialize():
    """
    ログデータを初期化する
    """
    logData.clear()


def log(role, prompt):
    """
    指定された話者と文字列からログを記録する。
    """
    # 発言日時を取得
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # 発言内容を整形
    formatted_prompt = {"role": role, "content": prompt, "datetime": now}
    # logDataに追加
    logData.append(formatted_prompt)


def saveJson():
    """
    ログデータをjson形式で保存する
    """
    # ファイル名を取得
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "log/" + now + ".json"
    # ログデータをjson形式で保存
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(logData, f, indent=4, ensure_ascii=False)