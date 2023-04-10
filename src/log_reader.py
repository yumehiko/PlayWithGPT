import os
import glob
import json

def ReadLatestJson() -> str:
    # フォルダ内の全てのファイルパスを取得し、新しいもの順にソートして最も新しいファイルを取得
    all_files = glob.glob("log/*.json")
    latest_file = max(all_files, key=os.path.getctime)

    # 最新ファイルを読み込んで、JSONの整形
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    formatted_data = []
    for message in data:
        formatted_message = {
            "role": message["role"],
            "content": message["content"],
            "datetime": message["datetime"]
        }
        formatted_data.append(formatted_message)

    # 整形したJSONを返す
    return json.dumps(formatted_data, ensure_ascii=False, indent=4)