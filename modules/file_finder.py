import os

def findFilePath(file_name: str, search_path : str) -> str:
  """
  search_path以下のフォルダ内で、指定したファイル名を持つファイルのパスを返す。
  該当するファイルがない場合は、空文字列を返す。
  """
  for root, dir, files in os.walk(search_path):
      if file_name in files:
          return os.path.join(root, file_name)
  return ""


def findSourceCode(file_name: str) -> str:
  """
  指定したファイル名の中身を文字列として返す。
  該当するファイルがない場合は、空文字列を返す。
  """

  search_path = os.path.dirname(os.path.abspath(__file__))
  file_path = findFilePath(file_name, search_path)

  # 該当するファイルがなかった場合は、空文字列を返す
  if not file_path:
    return ""
  
  # 該当するファイルがあった場合は、UTF-8エンコードでファイルを開いて中身を返す
  with open(file_path, "r", encoding="utf-8") as file:
    return file.read()