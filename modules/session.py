from modules.talker import Talker
from modules.talker_type import TalkerType
from modules.translater import Translater, TranslateType
from modules.chat_message import ChatMessage, ChatMessageSubject, SenderInfo
from modules import log_writer
from modules.translater import TranslateType, Language
from modules.abstract_ui import AbstractUI
from modules import code_generator
from abc import ABC, abstractmethod
from enum import Enum
import os
import yaml
from yaml import MappingNode
from typing import Union, IO
import shutil
import asyncio


class SessionType(Enum):
    none = 0
    cancel = 1
    one_on_one = 2
    bot_on_bot = 3
    auto_task = 4



class SessionConfig:
    def __init__(self, participant_names: list[str], session_type: SessionType, translate_type: TranslateType) -> None:
        self.participant_names = participant_names
        self.session_type = session_type
        self.translate_type = translate_type



class SessionConfigLoader(yaml.SafeLoader):
    def __init__(self, stream: Union[str, bytes, IO[str], IO[bytes]]) -> None:
        super().__init__(stream)

    def read_session_config(self, node: MappingNode) -> SessionConfig:
        data = self.construct_mapping(node)
        return SessionConfig(
            participant_names=data["participants"],
            session_type=SessionType[data["session_type"]],
            translate_type=TranslateType[data["translate_type"]]
        )

    
SessionConfigLoader.add_constructor("!SessionConfig", SessionConfigLoader.read_session_config)



class Session(ABC):
    def __init__(self, view: AbstractUI, system_talker: Talker, participants: list[Talker], type: SessionType, translate_type: TranslateType) -> None:
        self.view = view
        self.system_talker = system_talker
        self.participants = participants
        self.type = type
        self.translate_type = translate_type
        self.message_subject = ChatMessageSubject()
        self.is_end: bool = False
        self.skip: bool = False
    
    @property
    def has_translater(self) -> bool:
        return self.translater is not None

    def set_translater(self, translater: Translater) -> None:
        self.translater = translater


    async def begin(self) -> None:
        """
        会話を開始する。
        """
        manuals = [
            "=== PlayWithGPT ===",
            "Clear、またはcと入力すると、文脈をクリアします。",
            "Log、またはlと入力すると、最新のログを参照します（文脈には含まれない）。",
            "read: fileName.pyと入力すると、fileName.pyのソースコードをBotに対して読み上げます。",
            "End、またはeと入力すると、セッションを終了します。",
            "=== 会話を開始します ===",
        ]
        manual_text = "\n".join(manuals)
        self.view.print_message_as_system(manual_text, False)
        self.main_loop = asyncio.create_task(self.session_loop())
        
        try:
            await self.main_loop
        except asyncio.CancelledError:
            pass
        finally:
            self.write_as_yaml()
            self.view.print_message(ChatMessage("=== セッションを終了します ===", self.system_talker.sender_info))


    def send_to(self, message: ChatMessage, target: Talker) -> None:
        """
        指定した話者にメッセージを送信する。
        """
        if target.sender_info == message.sender_info:
            return
        target.receive_message(message)


    def send_to_all(self, message: ChatMessage) -> None:
        """
        会話に参加している全ての話者にメッセージを送信する。
        """
        for participant in self.participants:
            self.send_to(message, participant)
    

    def clear_context(self) -> None:
        """
        全員の会話のコンテキストをクリアする。
        """
        for participant in self.participants:
            participant.clear_context()
        self.view.print_message(ChatMessage("=== コンテキストをクリアしました ===", self.system_talker.sender_info))


    def write_as_yaml(self) -> None:
        participant_names = []
        for participant in self.participants:
            participant_names.append(participant.persona_name)
        config = {
                "participants": participant_names,
                "session_type": self.type.name,
                "translate_type": self.translate_type.name
        }

        with open("session_config.yaml", "w", encoding="utf-8") as outfile:
                outfile.write("!SessionConfig\n")
                yaml.dump(config, outfile, allow_unicode=True, explicit_start=False, default_flow_style=None, Dumper=yaml.SafeDumper)
    

    async def session_loop(self) -> None:
        while not self.is_end:
            try:
                await self.chat()
            except asyncio.CancelledError:
                raise

    @abstractmethod
    async def chat(self) -> None:
        """
        会話処理。
        """
        pass


    def print_message(self, message: ChatMessage) -> None:
        """
        メッセージをチャット欄に表示する。
        """
        self.view.print_message(message)

        # logすべきなら、logする。
        if message.should_log:
            log_writer.log(message)


    def end(self) -> None:
        """
        会話を終了する。
        """
        self.main_loop.cancel()


class OneOnOneSession(Session):
    """
    ユーザーとBotの1対1の会話を行う。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker, participants: list[Talker], translate_type: TranslateType) -> None:
        super().__init__(view, system_talker, participants, SessionType.one_on_one, translate_type)
    

    async def chat(self) -> None:
        """
        参加者全員が会話を1周行う。
        """
        for participant in self.participants:
            self.skip = False
            try:
                self.view.process_event()
                message = await participant.generate_message()
                self.view.process_event()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                if self.has_translater:
                    sender_is_user: bool = message.sender_info.type == TalkerType.user
                    printable_message = message
                    if sender_is_user:
                        message = await self.translater.translate(message, Language.EN)
                    else:
                        printable_message = await self.translater.translate(message, Language.JP)
                    self.view.process_event()
                self.send_to_all(message)
                self.print_message(printable_message)
            except asyncio.CancelledError:
                raise

class BotOnBotSession(Session):
    """
    Bot同士の会話を行う。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker, participants: list[Talker], translate_type: TranslateType) -> None:
        super().__init__(view, system_talker, participants, SessionType.bot_on_bot, translate_type)
 

    async def begin(self) -> None:
        # はじめに、ユーザーから議題の入力を受け取り、それをbot全員に送信する。
        self.view.print_message(ChatMessage("=== 議題を入力してください ===", self.system_talker.sender_info, False))
        topic = await self.view.request_user_input()
        topic = "議題：\n" + topic
        topic_message = ChatMessage(topic, self.system_talker.sender_info)
        self.send_to_all(topic_message)
        self.view.print_message(topic_message)
        return await super().begin()

    async def chat(self) -> None:
        """
        参加者全員が会話を1周行う。
        """
        for participant in self.participants:
            self.skip = False
            try:
                self.view.process_event()
                message = await participant.generate_message()
                self.view.process_event()
                self.message_subject.on_next(message)
                if self.skip:
                    return
                if self.has_translater:
                    printable_message = await self.translater.translate(message, Language.JP)
                    self.view.process_event()
                self.send_to_all(message)
                self.print_message(printable_message)

                # botが発言するたびに、ユーザーからの入力を5秒待ち、もし入力があった場合、セッションを終了する。
                # 入力がなかった場合、セッションを続行する。
                # TODO: set_place_holder()を実装する。
                # TODO: ユーザーからの入力を受け取ると、セッションを終了する。
            except asyncio.CancelledError:
                raise

class AutoTaskSession(Session):
    """
    Botがタスクを処理する。
    """
    def __init__(self, view: AbstractUI, system_talker: Talker, participants: list[Talker]) -> None:
        super().__init__(view, system_talker, participants, SessionType.auto_task, TranslateType.none)
        try:
            self.task = self.get_task()
        except FileNotFoundError as e:
            self.view.print_message(ChatMessage(e.strerror, self.system_talker.sender_info))
        

    def get_task(self) -> str:
        bot = self.participants[0]
        # tasksディレクトリ内にファイルがあるか確認する。
        # ファイルがあるなら、そのファイルを読み込み、userメッセージとしてbotに渡す。
        # ファイルがないなら、例外を返す。
        if not os.path.exists("tasks"):
            raise FileNotFoundError("tasksディレクトリがありません。")
        files = os.listdir("tasks")
        if len(files) == 0:
            raise FileNotFoundError("tasksディレクトリにファイルがありません。")
        # 0番目のファイルの内容をstrで取得する。
        with open("tasks/" + files[0], "r", encoding="utf-8") as infile:
            task = infile.read()
        user_info = SenderInfo("user", "User", TalkerType.user)
        bot.receive_message(ChatMessage(task, user_info, False))
        # ファイルを読み込んだことを、ファイル名を含んだメッセージで示す。
        self.view.print_message(ChatMessage(f"tasks/{files[0]}を読み込みました。", self.system_talker.sender_info))
        return task


    async def chat(self) -> None:
        # MEMO: ここにある処理は、NewModuleを生成するのみ。
        #       将来的には、生成したモジュールのテストも自動実行する必要がある。
        #       タスクファイルの拡張子は、タスクの種類ごとに「モジュール生成：.gm」「テスト：.nt」とする。
        #       モジュール生成後は、タスクファイルの拡張子を「.gm」から「.nt」に変更する。
        message = await self.participants[0].generate_message()
        self.view.process_event()
        self.print_message(message)
        # taskの拡張子をtaskからpyに変換し、file_nameとする
        module_name = self.task.replace(".task", ".py")
        task_file_path = os.path.join("tasks/", self.task)
        source_code = message.text
        code_generator.generate_module(module_name, source_code)
        # taskファイルをtests/ディレクトリに移動する。
        shutil.move(task_file_path, "tests/")
        # TODO: テストを実行する。

    # タスクファイルの拡張子から、タスクの種類を判別する。
    def get_task_type(self) -> str:
        """
        タスクファイルの拡張子から、タスクの種類を判別する。
        """
        task_type = ""
        if self.task.endswith(".gm"):
            task_type = "モジュール生成"
        elif self.task.endswith(".nt"):
            task_type = "テスト"
        return task_type