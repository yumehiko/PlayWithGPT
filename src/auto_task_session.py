# インポート
from .session import Session, SessionType
from .session import Session, SessionType
from .chat_message import ChatMessage, SenderInfo
from .talker import Talker
from .talker_type import TalkerType
from .gptBot import GPTBot
from .translater import TranslateType
from .abstract_ui import AbstractUI
from . import code_generator
from enum import Enum
import os
import shutil



class TaskType(Enum):
    none = 0
    code = 1 # コード生成
    test = 2 # テストコード生成
    refactoring = 3 # リファクタリング
    task = 4 # タスク生成
    rdd = 5 # 要件定義書生成



class GPTTask():
    """
    タスク。tasks/ディレクトリ以下から、.taskファイルを読み込む。
    """
    def __init__(self) -> None:
        self.dir_path = ""
        for root, dirs, file_names in os.walk("tasks"):
            # completedディレクトリを無視する
            if "completed" in dirs:
                dirs.remove("completed")
            for file_name in file_names:
                if file_name.endswith(".task"):
                    self.file_name = file_name
                    self.dir_path = root
        if not self.dir_path:
            raise FileNotFoundError("taskファイルがありません。")
        self.type = self.get_task_type(self.dir_path)
        with open(os.path.join(self.dir_path, self.file_name), "r", encoding= "utf-8") as f:
            self.content = f.read()


    @property
    def file_name_as_py(self) -> str:
        """
        taskファイルの拡張子をtaskからpyに変換して返す。
        """
        return self.file_name.replace(".task", ".py")

    @property
    def full_path(self) -> str:
        """
        taskファイルのファイル名も含めたパスを返す。
        """
        return os.path.join(self.dir_path, self.file_name)    

    def get_task_type(self, task_file_path: str) -> TaskType:
        """
        ファイルパスに含まれる文字列から、サブディレクトリを判別し、そこからタスクの種類を類推する。
        """

        if "coding" in task_file_path:
            return TaskType.code
        elif "testing" in task_file_path:
            return TaskType.test
        else:
            raise ValueError("taskファイルのパス" + task_file_path + "は不正です。")
        



class AutoTaskSession(Session):
    """
    Botがタスクを処理する。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker) -> None:
        super().__init__(view, system_talker, [], SessionType.auto_task, TranslateType.none)
    

    def create_bot(self, task_type: TaskType) -> GPTBot:
        # Taskに対応できるBotを生成する。
        bot_name: str
        if task_type == TaskType.code:
            bot_name = "coder"
        elif task_type == TaskType.test:
            bot_name = "test_coder"
        else:
            raise ValueError("taskファイルのパスが不正です。")
        bot = GPTBot(bot_name, self.system_talker)
        self.participants.append(bot)
        return bot
    
    async def code_task(self, bot: GPTBot, task: GPTTask) -> None:
        """
        コード生成タスクを処理する。
        """
        message = await bot.generate_message()
        self.view.process_event()
        self.print_message(message)
        # 出力をもとに、モジュールファイルを生成する。
        module_name = task.file_name_as_py
        source_code = message.text
        code_generator.generate_module(module_name, source_code)

        # taskファイルをtests/ディレクトリに移動する。
        test_dir = os.path.join("tasks", "testing")
        shutil.move(task.full_path, test_dir)

        info = "コードを生成しました。"
        self.print_message(ChatMessage(info, self.system_talker.sender_info))

    async def test_task(self, bot: GPTBot, task: GPTTask) -> None:
        """
        テストコード生成タスクを処理する。
        """
        # テストコードを生成する。
        message = await bot.generate_message()
        self.view.process_event()
        self.print_message(message)
        # taskの拡張子をtaskからpyに変換し、file_nameとする
        testcode_name = task.file_name.replace(".task", "_test.py")
        source_code = message.text
        code_generator.generate_module(testcode_name, source_code, "tests")
        
        # taskファイルをcompletedディレクトリに移動する。
        completed_dir = os.path.join("tasks", "completed")
        shutil.move(task.full_path, completed_dir)

        info = "テストコードを生成しました。"
        self.print_message(ChatMessage(info, self.system_talker.sender_info))


    async def chat(self) -> None:
        # MEMO: 現状の処理は、NewModuleを生成するのみ。
        #       将来的には、生成したモジュールのテストも自動実行する必要がある。

        # Taskを取得する。
        try:
            task = GPTTask()
        except FileNotFoundError as e:
            self.view.print_message(ChatMessage(str(e), self.system_talker.sender_info))
            self.is_end = True
        
        # Taskに対応できるBotを生成する。
        bot = self.create_bot(task.type)
        # Taskの内容をBotに伝える。
        user_info = SenderInfo("user", "User", TalkerType.user)
        bot.receive_message(ChatMessage(task.content, user_info, False))
        # ファイルを読み込んだことを、ファイル名を含んだメッセージで示す。
        self.view.print_message(ChatMessage(f"{task.file_name}を読み込みました。", self.system_talker.sender_info))
        
        
        if task.type == TaskType.code:
            await self.code_task(bot, task)
        elif task.type == TaskType.test:
            await self.test_task(bot, task)
        else:
            raise ValueError("taskファイルのパスが不正です。")
        
        self.is_end = True