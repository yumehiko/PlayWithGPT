from src.hippocampus import Hippocampus, TryEmptyInput
from src import file_finder
import os

def memory_code(file_name: str) -> None:
    """
    指定したファイルのソースコードを読み込んで、記憶する。
    """
    source_code = file_finder.read_file(file_name, "src")
    full_path = os.path.join("src", file_name)
    print(full_path)
    hippocampus.input_memory(full_path, source_code)

if __name__ == "__main__":
    hippocampus = Hippocampus()

    results = hippocampus.query_memory("Classes for bot-to-bot conversations", 3)
    print(results)
    query = f"Classes on which {results[0]} depends"
    results = hippocampus.query_memory(query, 3)
    print(results)