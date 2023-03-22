import yaml
import openai

# これまでの会話の文脈
context = []


def initialize(mode=""):
    """
    クラスを初期化する。APIキーを渡し、文脈を初期化する。
    """

    # 設定ファイルからAPIキーを読み込む
    with open("key.yaml") as key_file:
        config = yaml.safe_load(key_file)
        openai.api_key = config["openai"]["api_key"]

    # 文脈を初期化する
    clearContext()

    # モードを設定する
    if mode == "":
        return
    formatted_mode = {"role": "system", "content": mode}
    context.append(formatted_mode)


def sendSystemMessage(message):
    """
    role:systemとしてAPIにメッセージを送る
    """
    formatted_message = {"role": "system", "content": message}
    context.append(formatted_message)

def sendUserMessage(message):
    """
    role:userとしてAPIにメッセージを送る
    """
    formatted_message = {"role": "user", "content": message}
    context.append(formatted_message)


def ask(question_body):
    """
    GPT-3にこれまでの文脈に加えた質問を投げ、その本文を返し、文脈を記憶する。
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
