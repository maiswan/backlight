from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from ..command_base import CommandBase

class CommandSourceRgb(CommandBase):
    mode: Literal["source_rgb"] = "source_rgb"
    red: float = Field(ge=0, le=255, default=255)
    green: float = Field(ge=0, le=255, default=255)
    blue: float = Field(ge=0, le=255, default=255)
    is_static = True

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        for i in targets:
            buffer[i] = (self.red, self.green, self.blue)
        