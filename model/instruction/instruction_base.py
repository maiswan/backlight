from __future__ import annotations
from abc import ABC, abstractmethod
from asyncio import Event
from typing import Callable, List, Optional, Coroutine
from pydantic import BaseModel

class Instruction(BaseModel, ABC):
    identifier: str

class AlphaInstruction(Instruction, ABC):
    @abstractmethod
    def execute(self, current_alpha: List[float], led_count: int, redraw: Callable[[Optional[int]], None], stop: Event) -> Coroutine | None:
        ...

class ColorInstruction(Instruction, ABC):
    @abstractmethod
    def execute(self, current_red: List[int], current_green: List[int], current_blue: List[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: Event) -> Coroutine | None:
        ...

class GammaInstruction(Instruction, ABC):
    @abstractmethod
    def execute(self, current_gamma: List[float], redraw: Callable[[Optional[int]], None], stop: Event) -> Coroutine | None:
        ...