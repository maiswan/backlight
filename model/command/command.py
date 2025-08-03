from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar, Iterable, List
from uuid import uuid4
from pydantic import BaseModel, Field

class CommandBase(BaseModel, ABC):
    mode: ClassVar[str]                       # discriminator
    id: str = Field(default_factory=uuid4)
    name: str = ""                            # user-friendly name
    z_index: int = 0                          # higher = rendered later
    targets: str = ""                         # LED indices, example: "1, 2, 3, 56-72"
    is_static: ClassVar[bool] = False            # set to true if this Command does not depend on the time
    is_enabled: bool = True

    def execute(self, current_red: List[float], current_green: List[float], current_blue: List[float], led_count: int, time: float):
        if (not self.is_enabled):
            return

        targets = self._toTargetList(led_count)
        self._compute(current_red, current_green, current_blue, targets, time)

    def _toTargetList(self, led_count: int):
        if self.targets == "":
            return range(led_count)

        output = []
        ranges = self.targets.replace(",", " ").split()

        for item in ranges:
            if item.isdigit():
                output.append(int(item))
                continue

            item_range = item.split("-")
            start = int(item_range[0])
            end = int(item_range[1])
            output.extend(range(start, end+1))

        return output

    @abstractmethod
    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        ...
