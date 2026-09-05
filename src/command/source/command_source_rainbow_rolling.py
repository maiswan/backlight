from typing import Iterable, Literal
from pydantic import Field
from ..command_base import CommandBase
from .hsvToRgb import hsvToRgb
from ...renderer import RgbBuffer

class CommandSourceRainbowRolling(CommandBase):
    mode: Literal["source_rainbow_rolling"] = "source_rainbow_rolling" # type: ignore
    is_static = False

    period: int = Field(ge=1000, default=5000)
    wavelength: int = Field(ge=1, default=64)
    saturation: float = Field(ge=0, le=1, default=1)
    propagation: int = Field(ge=0, le=1, default=1)

    def _compute(self, buffer: RgbBuffer, targets: Iterable[int], time: float):
        
        direction = -1 if self.propagation == 0 else 1

        for (index, i) in enumerate(targets):
            physical_position = (index % self.wavelength) / self.wavelength
            time_position = (time % self.period) / self.period                
            
            hue = (physical_position + time_position * direction) % 1.0 * 360
            r, g, b = hsvToRgb(hue, self.saturation, 1.0)

            buffer[i] = (r, g, b)
    
        