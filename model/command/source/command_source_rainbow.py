from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from ..command_base import CommandBase
from .hsvToRgb import hsvToRgb

class CommandSourceRainbow(CommandBase):
    mode: Literal["source_rainbow"] = "source_rainbow"
    period: int = Field(..., ge=1000)
    saturation: float = Field(..., ge=0, le=1)
    is_static = False

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        hue = (time * 1000 % self.period) / self.period * 360
        r, g, b = hsvToRgb(hue, self.saturation, 1.0)

        for i in targets:
            buffer[i] = (r, g, b)
    
        