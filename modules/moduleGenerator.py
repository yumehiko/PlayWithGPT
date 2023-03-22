

def write_py_file(chat_text):
    """
    チャットの発言を元に.pyファイルを書き出し、そのファイル名を返す。
    chat_textには、ファイル名から始まる発言が含まれている。
    """

    # .pyまでを抜き出し、ファイル名とする。
    file_name = "modules/" + chat_text.split(".py")[0] + ".py"
    
    
    # chat_textにpythonコードブロックが含まれている場合、その中身を抜き出す。
    if "```python" in chat_text:
        source_code = split_by_pythoncodeBlock(chat_text)
    # chat_textにpythonコードブロックが含まれておらず、かつコードブロックはある場合、コードブロックで抜き出す。
    elif "```" in chat_text:
        source_code = split_by_codeBlock(chat_text)
    # chat_textにpythonコードブロックもコードブロックも含まれていない場合、ファイル名以後を抜き出す。
    else:
        source_code = split_by_fileName(chat_text)

    # .pyファイルに書き出す
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(source_code)
    
    return file_name

def split_by_pythoncodeBlock(chat_text):
    source_code = chat_text.split("```python")[1]
    source_code = source_code.split("```")[0]
    return source_code

def split_by_codeBlock(chat_text):
    source_code = chat_text.split("```")[1]
    return source_code

def split_by_fileName(chat_text):
    source_code = chat_text.split(".py")[1]
    return source_code