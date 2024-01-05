from .session import Session, SessionType
from .translater import Translater, TranslateType, Language
from .abstract_ui import AbstractUI
from .chat_message import ChatMessage
from .talker import Talker
from .bot_agent import BotAgent
from . import file_finder
import asyncio

class AgiSession(Session):
    """
    自律型タスク解決セッション。
    """

    def __init__(self, view: AbstractUI, system_talker: Talker, user: Talker, translate_type: TranslateType) -> None:
        super().__init__(view, system_talker, [], SessionType.agi, translate_type)
        self.user = user
        
    async def chat(self) -> None:
        # 1. goalを受ける
        # 2. goalをtasksに分割する
        # 3. tasksを解決可能なresolvablesとunresolvablesに分割する
        # 4. unresolvablesをもとに、追加すべき機能をまとめ、need_function_tasksとする
        # 5. need_function_tasksをresolvablesとunresolvablesに分割し、それぞれに分配する。
        # 6. 4-5を繰り返し、unresolvablesが空になるまで繰り返す
        # 7. resolvablesを解決する
        agent = BotAgent()  
        objective = await self.ask_objective()
        context = await self.ask_context()
        feasibility = self.feasibility_assessment(agent, objective, context)
        if not feasibility:
            text = f"Error: 目的が達成できない可能性があります。\n目的設定からやり直してください。"
            self.print_message_as_system(text, True)
            return


        tasks = self.split_to_tasks(agent, objective)
        resolvables, unresolvables = self.split_to_resolvables(agent, objective, tasks)
        
        self.is_end = True
    
    async def ask_objective(self) -> str:
        """
        ユーザーから、目的の設定の入力を受ける。
        """
        text = f"目的を入力してください。\n例：気の利いた挨拶を1つ提案してください。"
        self.print_message_as_system(text, True)
    
        try:
            objective = await self.view.request_user_input()
            if not objective:
                raise ValueError("目的が入力されていません。")
        except asyncio.CancelledError:
            raise
        
        text = "Objective: " + objective
        message = ChatMessage(text, self.user.sender_info, True)
        self.print_message(message)

        return objective
    
    async def ask_context(self) -> str:
        """
        ユーザーから、目的設定に関する文脈の入力を受ける。
        """
        text = f"目的に関する文脈を入力してください。\n例：久々の友人との会話で、挨拶をする場面。"
        self.print_message_as_system(text, True)

        try:
            context = await self.view.request_user_input()
            self.view.process_event()
        except asyncio.CancelledError:
            raise
        text = "Context: " + context
        message = ChatMessage(text, self.user.sender_info, True)
        self.print_message(message)

        return context
                

    def split_to_tasks(self, agent: BotAgent, objective: str) -> list[str]:
        prompt = f"""
        You are an AI listing tasks to be performed based on the following objective: {objective}.
        You are part of a repository called PlayWithGPT and this objective must be resolved by PlayWithGPT alone.
        Subdivide and list the objectives into tasks in order to resolve them. Do not try to solve them at this point.
        The list should be formatted with the "-" sign and should not include responses other than the list.
        Response:"""
        response = agent.response_to_prompt(prompt)
        self.view.process_event()
        tasks = response.split("\n") if "\n" in response else [response]

        # tasksを表示する
        self.print_message_as_system("=== Task List ===", True)
        tasks_text = "\n".join(tasks)
        self.print_message_as_system(tasks_text, True)

        return tasks
    
    def split_to_resolvables(self, agent: BotAgent, objective: str, tasks: list[str]) -> tuple[list[str], list[str]]:
        abilities = file_finder.read_file("abilities.txt", "documents")
        first_command = {"role": "system", "content": f"""
        You are an AI that divides the following task list {tasks} into those that can be solved at this time and those that cannot be solved based on the following objective {objective}.
        You are part of a repository called PlayWithGPT and this objective must be resolved by PlayWithGPT alone.
        The current ablities of PlayWithGPT is as follows: 
        {abilities}
        Identify and list only those issues that PlayWithGPT can specifically solve. Ignore issues that cannot be solved.
        The list should be formatted with the "-" sign and should not include responses other than the list.
        Response:"""
        }
        context : list[dict[str, str]] = [first_command]        

        response = agent.response_to_context(context)
        self.view.process_event()
        resolvables = response.split("\n") if "\n" in response else [response]
        self_response = {"role": "assistant", "content": response}
        context.append(self_response)

        second_command = {"role": "system", "content": f"""
        Next, list the issues that cannot be resolved.
        If there is no issue that cannot be resolved, just return "Nothing".
        Response:"""
        }
        context.append(second_command)
        response = agent.response_to_context(context)
        self.view.process_event()
        unresolvables = response.split("\n") if "\n" in response else [response]

        # resolvablesを表示する
        self.print_message_as_system("=== Resolvable Task List ===", True)
        resolvables_text = "\n".join(resolvables)
        self.print_message_as_system(resolvables_text, True)

        # unresolvablesを表示する
        self.print_message_as_system("=== Unresolvable Task List ===", True)
        unresolvables_text = "\n".join(unresolvables)
        self.print_message_as_system(unresolvables_text, True)

        return resolvables, unresolvables


    def feasibility_assessment(self, agent: BotAgent, objective: str, context: str) -> bool:
        """
        目的の実現可能性を判定する。
        """

        text = "目的の実現可能性を判定します……"
        self.print_message_as_system(text, True)

        abilities = file_finder.read_file("abilities.txt", "documents")
        prompt = f"""
        You are an AI that determines if the objective given by the user are feasible.
        You are part of a repository called PlayWithGPT.
        PlayWithGPT is capable of: 
        {abilities}
        Based on the above, determine whether or not the following objective is feasible.
        Response with a simple "Yes" or "No”.
        Objective: {objective}
        Context: {context}
        Response: 
        """
        response = agent.response_to_prompt(prompt)
        self.view.process_event()

        return "Yes" in response