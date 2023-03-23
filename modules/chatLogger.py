import json
from datetime import datetime
from modules.loggableMessage import LoggableMessage
from typing import List, Dict

# logData: ログデータを格納するリスト
logData: List[Dict[str, str]] = []


def initialize():
    """
    ログデータを初期化する
    """
    logData.clear()


def log(message: LoggableMessage):
    """
    指定された話者と文字列からログを記録する。
    """

    # ログを記録しない場合は何もしない
    if not message.should_log:
        return

    # 発言日時を取得
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # 発言内容を整形
    formatted_prompt = {"role": message.talker.name,
                        "content": message.text,
                        "datetime": now}
    # logDataに追加
    logData.append(formatted_prompt)


def saveJson():
    """
    これまでに記録したログデータをjson形式で保存する
    """
    # ファイル名を取得
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "log/" + now + ".json"
    # ログデータをjson形式で保存
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(logData, f, indent=4, ensure_ascii=False)
