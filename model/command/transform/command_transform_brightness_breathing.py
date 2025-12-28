from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from math import sin
from ..command_base import CommandBase

class CommandTransformBrightnessBreathing(CommandBase):
    mode: Literal["transform_brightness_breathing"] = "transform_brightness_breathing"
    min_brightness: float = Field(ge=0.0, le=4.0, default=0.0)
    max_brightness: float = Field(ge=0.0, le=4.0, default=1.0)
    period: float = Field(ge=1000, default=5000)
    is_static = False

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        brightness = sin(2 * 3.14 * time * 1000 / self.period) / 2 + 0.5
        brightness *= self.max_brightness - self.min_brightness
        brightness += self.min_brightness

        for i in targets:
            r = buffer[i][0] * brightness
            g = buffer[i][1] * brightness
            b = buffer[i][2] * brightness
            buffer[i] = (r, g, b)
        