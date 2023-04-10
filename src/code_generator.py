import os


def generate_module(file_name: str, source_code: str, directory: str = "src") -> str:
    """
    ファイル名とソースコードから、.pyファイルを生成し、そのパスを返す。
    """

    # codeにpythonコードブロックが含まれている場合、その中身を抜き出す。
    if "```python" in source_code:
        source_code = split_by_pythoncodeBlock(source_code)
    # codeにpythonコードブロックが含まれておらず、かつコードブロックはある場合、コードブロックで抜き出す。
    elif "```" in source_code:
        source_code = split_by_codeBlock(source_code)
    # codeにpythonコードブロックもコードブロックも含まれていない場合、そのままソースコードを使用する。
    else:
        pass

    # .pyファイルに書き出す
    result_path = os.path.join(directory, file_name)
    with open(result_path, 'w', encoding="utf-8") as f:
        f.write(source_code)
    
    return result_path


def split_by_pythoncodeBlock(chat_text: str) -> str:
    source_code = chat_text.split("```python")[1]
    source_code = source_code.split("```")[0]
    return source_code


def split_by_codeBlock(chat_text: str) -> str:
    splitted = chat_text.split("```")
    if len(splitted) >= 3:
        source_code = splitted[1]
    else:
        source_code = splitted[0]
    return source_code


def split_by_fileName(chat_text: str) -> str:
    source_code = chat_text.split(".py")[1]
    return source_code
