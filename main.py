import gptContact


def main():
    """
    GPT-3との会話を開始する
    """

    gptContact.initialize()
    question = "こんにちは。私はたかしです。"
    response = gptContact.ask(question)
    print(response)
    question = "あなたは何ができますか？　簡潔に答えて。"
    response = gptContact.ask(question)
    print(response)
    question = "私の名前を覚えていますか？"
    response = gptContact.ask(question)
    print(response)


# これは、このファイルが直接実行された場合にのみ実行されます。
if __name__ == "__main__":
    main()
