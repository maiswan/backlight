
from abc import ABC, abstractmethod
from pydantic import BaseModel

class PixelBase(BaseModel, ABC):
    @property
    @abstractmethod
    def pixels(self):
        ...

    @abstractmethod
    def __getitem__(self, key):
        ...

    @abstractmethod
    def __setitem__(self, key, value):
        ...

    @abstractmethod
    def __init__(self, pin: int, count: int, pixel_order: str):
        ...

    @abstractmethod
    def show(self):
        ...

    @abstractmethod
    def clear(self):
        ...

    