


import os
import glob
import json

# フォルダ内の全てのファイルパスを取得し、新しいもの順にソートして最も新しいファイルを取得
all_files = glob.glob("log/*.json")
latest_file = max(all_files, key=os.path.getctime)

# 最新ファイルを読み込んで、JSONの整形
with open(latest_file, "r") as f:
    data = json.load(f)

formatted_data = []
for message in data:
    formatted_message = {
        "speaker": message["role"],
        "content": message["content"],
        "time": message["datetime"]
    }
    formatted_data.append(formatted_message)

# 整形したJSONを出力
print(json.dumps(formatted_data, ensure_ascii=False, indent=4))
 

このコードでは、`glob`モジュールを使用してフォルダ内のJSONファイルのパスをリストで取得し、その中から最も新しいファイルを選択します。そして、`json`モジュールを使用してJSONファイルを読み込み、必要な情報を整形します。最後に、`json.dumps()`関数を使用して整形したJSONを表示します。