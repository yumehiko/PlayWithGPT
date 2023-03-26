import os


def find_file_path(file_name: str) -> str:
    """
    リポジトリ内で、指定したファイル名を持つファイルのパスを返す。
    該当するファイルがない場合は、空文字列を返す。
    """
    # モジュールファイルの親ディレクトリ
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print(repo_path)

    # リポジトリ直下とサブディレクトリをすべて探索する
    for root, dirs, files in os.walk(repo_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""


def read_file(file_name: str) -> str:
    """
    指定したファイル名の中身を文字列として返す。
    該当するファイルがない場合は、空文字列を返す。
    """

    file_path = find_file_path(file_name)

    # 該当するファイルがなかった場合は、空文字列を返す
    if not file_path:
        return ""

    # 該当するファイルがあった場合は、UTF-8エンコードでファイルを開いて中身を返す
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
