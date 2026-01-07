from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from math import sin
from ..command_base import CommandBase

class CommandTransformBrightnessRolling(CommandBase):
    mode: Literal["transform_brightness_rolling"] = "transform_brightness_rolling"
    min_brightness: float = Field(ge=0.0, le=4.0, default=0.0)
    max_brightness: float = Field(ge=0.0, le=4.0, default=1.0)
    period: int = Field(ge=1000, default=5000)
    wavelength: int = Field(ge=1, default=64)
    propagation: int = Field(ge=0, le=1, default=1)
    is_static = False

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        direction = -1 if self.propagation == 0 else 1

        for (index, i) in enumerate(targets):
            physical_position = (index % self.wavelength) / self.wavelength
            time_position = ((time * 1000) % self.period) / self.period                
            
            brightness = (physical_position + time_position * direction) % 1.0
            brightness = sin(brightness * 2 * 3.14) / 2 + 0.5
            brightness *= self.max_brightness - self.min_brightness
            brightness += self.min_brightness
            
            r = buffer[i][0] * brightness
            g = buffer[i][1] * brightness
            b = buffer[i][2] * brightness
            buffer[i] = (r, g, b)
        