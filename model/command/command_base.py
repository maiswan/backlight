from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar, Iterable
from uuid import uuid4
from pydantic import BaseModel, Field
from ..buffer_types import RgbBuffer

class CommandBase(BaseModel, ABC):
    mode: ClassVar[str]                                 # discriminator
    
    id: str = Field(default_factory=uuid4)
    name: str = ""                                      # user-friendly name
    
    z_index: int = Field(default=0)                     # higher = rendered later
    alpha: float = Field(ge=0.0, le=1.0, default=1.0)

    targets: str = ""                                   # LED indices, example: "1, 2, 3, 56-72"
    _prev_targets: str | None = None
    _target_indices: list[int] | None = None

    @property
    def target_indices(self):
        return self._target_indices

    def clear_target_cache(self):
        self._prev_targets = None

    is_static: ClassVar[bool] = False                   # set to true if this Command does not depend on the time
    is_enabled: bool = True

    def execute(self, buffer: RgbBuffer, led_count: int, time: float):
        if (not self.is_enabled):
            return

        if (self.targets != self._prev_targets):
            self._target_indices = self.compile_targets(led_count)
            self._prev_targets = self.targets

        self._compute(buffer, self.target_indices, time)

    def compile_targets(self, led_count: int):
        if not self.targets:
            return list(range(led_count))

        indices: set[int] = set()

        for item in self.targets.replace(",", " ").split():
            if "-" in item:
                start, end = item.split("-", 1)
                indices.update(range(int(start), int(end) + 1))
            else:
                indices.add(int(item))

        return sorted(indices)


    @abstractmethod
    def _compute(self, buffer: RgbBuffer, targets: Iterable[int], time: float):
        ...
