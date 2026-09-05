from typing import Iterable, Literal
from pydantic import Field
from ..command_base import CommandBase
from .hsvToRgb import hsvToRgb
from ...renderer import RgbBuffer

class CommandSourceHsv(CommandBase):
    mode: Literal["source_hsv"] = "source_hsv" # type: ignore
    is_static = True
    
    hue: float = Field(ge=0, le=360, default=0)
    saturation: float = Field(ge=0, le=1, default=1)
    value: float = Field(ge=0, le=1, default=1)

    def _compute(self, buffer: RgbBuffer, targets: Iterable[int], time: float):
        r, g, b = hsvToRgb(self.hue, self.saturation, self.value)
        for i in targets:
            buffer[i] = (r, g, b)
    
        