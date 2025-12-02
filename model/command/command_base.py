from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar, Iterable, List
from uuid import uuid4
from pydantic import BaseModel, Field

class CommandBase(BaseModel, ABC):
    mode: ClassVar[str]                        # discriminator
    
    id: str = Field(default_factory=uuid4)
    name: str = ""                             # user-friendly name
    
    z_index: int = 0                           # higher = rendered later
    alpha: float = Field(..., ge=0.0, le=1.0)
    targets: str = ""                          # LED indices, example: "1, 2, 3, 56-72"
    
    is_static: ClassVar[bool] = False          # set to true if this Command does not depend on the time
    is_enabled: bool = True

    def execute(self, buffer: List[tuple[float, float, float]], led_count: int, time: float):
        if (not self.is_enabled):
            return

        targets = self.get_targets(led_count)
        self._compute(buffer, targets, time)

    def get_targets(self, led_count: int):
        if not self.targets:
            yield from range(led_count)
            return

        for item in self.targets.replace(",", " ").split():
            if not item:
                continue

            if item.isdigit():
                yield int(item)
                continue

            if "-" in item:
                parts = item.split("-", 1)
                if len(parts) == 2:
                    start = int(parts[0])
                    end = int(parts[1])
                    yield from range(start, end + 1)

    @abstractmethod
    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        ...
