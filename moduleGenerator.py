

def write_py_file(chat_text):
    """
    チャットの発言を元に.pyファイルを書き出し、そのファイル名を返す。
    chat_textには、ファイル名から始まる発言が含まれている。
    """

    # 1行目を抜き出し、それをファイル名とする。
    file_name = chat_text.split("\n")[0]
    
    # 1行目を削除し、残りのテキストをコードとする。
    code_text = chat_text.replace(file_name, "")

    # コードから、コードブロックなどを削除する。
    code_text = code_text.replace("```python", "")
    code_text = code_text.replace("```", "")

    # .pyファイルに書き出す
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(code_text)
    
    return file_name