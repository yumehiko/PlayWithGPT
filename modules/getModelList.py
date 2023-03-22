import yaml
import openai
import json

# openaiのmodelsのlistを取得する。
with open("key.yaml") as key_file:
    config = yaml.safe_load(key_file)
    openai.api_key = config["openai"]["api_key"]
model_list = openai.Model.list()

file_name = "modelList.json"

with open(file_name, 'w', encoding="utf-8") as f:
    f.write(json.dumps(model_list))