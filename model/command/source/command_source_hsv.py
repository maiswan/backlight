from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from .command_source_base import CommandSourceBase
from .hsvToRgb import hsvToRgb

class CommandSourceHsv(CommandSourceBase):
    mode: Literal["source_hsv"] = "source_hsv"
    hue: float = Field(ge=0, le=360, default=0)
    saturation: float = Field(ge=0, le=1, default=1)
    value: float = Field(ge=0, le=1, default=1)
    is_static = True

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        r, g, b = hsvToRgb(self.hue, self.saturation, self.value)
        for i in targets:
            buffer[i] = (r, g, b)
    
        