from typing import Iterable, Literal
from pydantic import Field
from ..command_base import CommandBase
from .hsvToRgb import hsvToRgb
from ...renderer import RgbBuffer

class CommandSourceRainbow(CommandBase):
    mode: Literal["source_rainbow"] = "source_rainbow" # type: ignore
    is_static = False

    period: int = Field(ge=1000, default=5000)
    saturation: float = Field(ge=0, le=1, default=1.0)

    def _compute(self, buffer: RgbBuffer, targets: Iterable[int], time: float):
        hue = (time % self.period) / self.period * 360
        r, g, b = hsvToRgb(hue, self.saturation, 1.0)

        for i in targets:
            buffer[i] = (r, g, b)
    
        