from typing import Iterable, Literal
from pydantic import Field
from ..command_base import CommandBase
from ...renderer import RgbBuffer

class CommandSourceRgb(CommandBase):
    mode: Literal["source_rgb"] = "source_rgb" # type: ignore
    is_static = True
    
    red: float = Field(ge=0, le=255, default=255)
    green: float = Field(ge=0, le=255, default=255)
    blue: float = Field(ge=0, le=255, default=255)

    def _compute(self, buffer: RgbBuffer, targets: Iterable[int], time: float):
        r = self.red / 255.0
        g = self.green / 255.0
        b = self.blue / 255.0
        for i in targets:
            buffer[i] = (r, g, b)
        