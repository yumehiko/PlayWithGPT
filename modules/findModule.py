import os

def findFilePath(file_name: str) -> str:
  """
  search_path以下のフォルダ内で、指定したファイル名を持つファイルのパスを返す。
  該当するファイルがない場合は、空文字列を返す。
  """
  for root, dir, files in os.walk("modules"):
      if file_name in files:
          return os.path.join(root, file_name)
  return ""


def findSourceCode(file_name: str) -> str:
  """
  search_path以下のフォルダ内から、指定したファイル名の中身を文字列として返す。
  該当するファイルがない場合は、空文字列を返す。
  """

  # をインポートして、指定したファイル名を持つファイルのパスを取得する
  file_path = findFilePath(file_name)

  # 該当するファイルがなかった場合は、空文字列を返す
  if not file_path:
    return ""
  
  # 該当するファイルがあった場合は、ファイルを開いて中身を返す
  with open(file_path, "r", encoding="utf-8") as file:
    return file.read()