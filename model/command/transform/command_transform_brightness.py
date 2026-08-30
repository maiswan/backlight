from typing import Iterable, Literal
from pydantic import Field
from ..command_base import CommandBase
from ...buffer_types import RgbBuffer

class CommandTransformBrightness(CommandBase):
    mode: Literal["transform_brightness"] = "transform_brightness"
    brightness: float = Field(ge=0.0, le=4.0, default=1.0)
    is_static = True

    def _compute(self, buffer: RgbBuffer, targets: Iterable[int], time: float):
        for i in targets:
            r = buffer[i][0] * self.brightness
            g = buffer[i][1] * self.brightness
            b = buffer[i][2] * self.brightness
            buffer[i] = (r, g, b)
        