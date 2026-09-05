
from abc import ABC, abstractmethod
from typing import Any, Literal
from pydantic import BaseModel
from ..renderer.buffer_types import RgbTuple

class PixelBase(BaseModel, ABC):

    @abstractmethod
    def __enter__(self) -> Any:
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> Literal[False]:
        ...

    @abstractmethod
    def __getitem__(self, key: int) -> Any:
        ...

    @abstractmethod
    def __setitem__(self, key: int, value: RgbTuple) -> None:
        ...

    @abstractmethod
    def show(self) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    