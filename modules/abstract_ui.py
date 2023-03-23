

from abc import ABC, abstractmethod
from modules.loggableMessage import LoggableMessage


class AbstractUI(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def print_manual(self):
        pass

    @abstractmethod
    def user_input(self) -> str:
        pass

    @abstractmethod
    def print_message(self, message: LoggableMessage) -> None:
        pass