

def write_py_file(chat_text):
    """
    チャットの発言を元に.pyファイルを書き出し、そのファイル名を返す。
    chat_textには、ファイル名から始まる発言が含まれている。
    """

    # .pyまでを抜き出し、ファイル名とする。
    file_name = "modules/" + chat_text.split(".py")[0] + ".py"
    
    # コードブロックの中身を抜き出し、ソースコードとする。
    source_code = chat_text.split("```python")[1]
    source_code = source_code.split('\n', 1)[1]
    source_code = source_code.split("```")[0]

    # .pyファイルに書き出す
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(source_code)
    
    return file_name