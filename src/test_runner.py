import subprocess
import os



class TestResult():
    def __init__(self, test_name: str, stdout: str, stderr: str):
        self.test_name = test_name
        self.stdout = stdout
        self.stderr = stderr
        self.has_error = len(stderr) > 0
    
    def print(self) -> None:
        print(f"テスト名: {self.test_name}")
        print(f"テスト結果: {self.stdout}")
        print(f"エラー: {self.stderr}")



class TestRunner():
    def run_tests(self, test_file_name: str) -> TestResult:
        tests_dir = "tests"
        test_file_path = os.path.join(tests_dir, test_file_name)
        command = f"python -m pytest {test_file_path}"
        run_result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # テスト結果の出力を取得
        stdout = run_result.stdout.strip()
        stderr = run_result.stderr.strip()

        result = TestResult(test_file_name, stdout, stderr)
        return result
