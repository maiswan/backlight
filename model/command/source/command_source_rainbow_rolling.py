from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from .command_source_base import CommandSourceBase
from .hsvToRgb import hsvToRgb

class CommandSourceRainbowRolling(CommandSourceBase):
    mode: Literal["source_rainbow_rolling"] = "source_rainbow_rolling"
    period: int = Field(ge=1000, default=5000)
    wavelength: int = Field(ge=1, default=64)
    saturation: float = Field(ge=0, le=1, default=1)
    propagation: int = Field(ge=0, le=1, default=1)
    is_static = False

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        
        direction = -1 if self.propagation == 0 else 1

        for (index, i) in enumerate(targets):
            physical_position = (index % self.wavelength) / self.wavelength
            time_position = ((time * 1000) % self.period) / self.period                
            
            hue = (physical_position + time_position * direction) % 1.0 * 360
            r, g, b = hsvToRgb(hue, self.saturation, 1.0)

            buffer[i] = (r, g, b)
    
        