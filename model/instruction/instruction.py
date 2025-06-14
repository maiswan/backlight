from __future__ import annotations
from abc import ABC, abstractmethod
from typing import  ClassVar, Iterable, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class InstructionBase(BaseModel, ABC):
    identifier: ClassVar[str]                 # discriminator
    id: UUID = Field(default_factory=uuid4)   # UUID for endpoints
    z_index: int = 0                          # higher = rendered later
    targets: Optional[list[int]] = None       # LED indices this instruction applies to, leave None to apply to all LEDs
    is_enabled: bool = True

    def execute(self, current_red: List[float], current_green: List[float], current_blue: List[float], led_count: int, time: float):
        if (not self.is_enabled):
            return

        targets = self.targets if self.targets else range(led_count)
        self._compute(current_red, current_green, current_blue, targets, time)

    @abstractmethod
    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        ...
