
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

    @property
    @abstractmethod
    def brightness(self):
        ...

    @brightness.setter
    def brightness(self, value: float):
        ...

    @abstractmethod
    def __init__(self, pin: int, count: int, pixel_order: str):
        ...

    @abstractmethod
    def show(self):
        ...

    