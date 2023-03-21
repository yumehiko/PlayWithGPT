import yaml
import openai

# これまでの会話のコンテキストの配列
context = []


def initialize():
    """
    クラスを初期化する。APIキーを渡し、文脈を初期化する。
    """

    # 設定ファイルからAPIキーを読み込む
    with open("key.yaml") as key_file:
        config = yaml.safe_load(key_file)
        openai.api_key = config["openai"]["api_key"]

    # 文脈を初期化する
    clearContext()


def ask(question_body):
    """
    GPT-3にこれまでの文脈に加えた質問を投げ、その本文を返し、文脈を記録する。
    """

    # APIKeyが設定済みか確認し、Keyが無い場合は例外を返す
    if openai.api_key is None:
        raise ValueError("APIKey is not set.")

    formatted_question = {"role": "user", "content": question_body}

    # 文脈があるなら、文脈を追加する。
    if not context:
        prompts = [formatted_question]
    else:
        prompts = context + [formatted_question]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts,
    )

    # 返答を整形する。
    response_body = response["choices"][0]["message"]["content"]
    formatted_response = {"role": "assistant", "content": response_body}

    # 文脈を追記する
    context.append(formatted_question)
    context.append(formatted_response)

    return response_body


def clearContext():
    """
    文脈をクリアする
    """
    context.clear()
