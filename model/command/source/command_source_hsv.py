from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from ..command_base import CommandBase

class CommandSourceHsv(CommandBase):
    mode: Literal["source_hsv"] = "source_hsv"
    hue: float = Field(..., ge=0, le=360)
    saturation: float = Field(..., ge=0, le=1)
    value: float = Field(..., ge=0, le=1)
    is_static = True

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        r, g, b = self._hsvToRgb()
        for i in targets:
            buffer[i] = (r, g, b)

    def _hsvToRgb(self):
        h = self.hue
        s = self.saturation
        v = self.value

        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        r, g, b = 0, 0, 0

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        elif 300 <= h < 360:
            r, g, b = c, 0, x

        r = (r + m) * 255
        g = (g + m) * 255
        b = (b + m) * 255

        return r, g, b
        