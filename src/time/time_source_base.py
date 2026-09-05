from abc import ABC, abstractmethod
from pydantic import BaseModel

class TimeSourceBase(BaseModel, ABC):
    @abstractmethod
    def advance(self, duration: int):
        ...

    @abstractmethod
    def now(self) -> int:
        ...

    