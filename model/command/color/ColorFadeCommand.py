import copy
import math
from time import monotonic
from typing import Iterable, Literal

from pydantic import Field
from model.command.command import CommandBase

class ColorFadeCommand(CommandBase):
    mode: Literal["color_fade"] = "color_fade"
    period: float = Field(..., ge=0)
    red: float = Field(..., ge=0, le=255)
    green: float = Field(..., ge=0, le=255)
    blue: float = Field(..., ge=0, le=255)
    _start_red: list[float] = []
    _start_green: list[float] = []
    _start_blue: list[float] = []
    _start_time: float
    is_static = False

    def _compute(self, current_red: list[float], current_green: list[float], current_blue: list[float], targets: Iterable[int], time: float):
        if (len(self._start_red) == 0):
            self._start_red = copy.deepcopy(current_red)
            self._start_green = copy.deepcopy(current_green)
            self._start_blue = copy.deepcopy(current_blue)
            self._start_time = monotonic()
            
        linear_percentage = min(1.0, (time - self._start_time) / (self.period / 1000))
        eased_percentage = -1 * math.cos(math.pi * linear_percentage) / 2 + 0.5  # Cosine easing
        for i in targets:
            red, green, blue = self.lerp(
                self._start_red[i],
                self._start_green[i],
                self._start_blue[i],
                self.red,
                self.green,
                self.blue,
                eased_percentage
            )
            current_red[i] = red
            current_green[i] = green
            current_blue[i] = blue

    def lerp(self, r1: float, g1: float, b1: float, r2: float, g2: float, b2: float, t: float):
        r = (1 - t) * r1 + t * r2
        g = (1 - t) * g1 + t * g2
        b = (1 - t) * b1 + t * b2
        return r, g, b
