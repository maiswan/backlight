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
            red, green, blue = self.lerp_rgb(
                (self._start_red[i], self._start_green[i], self._start_blue[i]),
                (self.red, self.green, self.blue),
                eased_percentage
            )
            current_red[i] = red
            current_green[i] = green
            current_blue[i] = blue

        # animation has completed, reset values in case this command is reused
        # if abs(eased_percentage - 1) < 0.001:
        #     self._start_red = []
        #     self._start_green = []
        #     self._start_blue = []
        #     self._start_time = 0
            
    def lerp_rgb(self, rgb1: tuple[float, float, float], rgb2: tuple[int, int, int], t: float):
        to_linear = lambda c: (c / 255) ** 2.2
        to_srgb = lambda c: round((c ** (1 / 2.2)) * 255)
        return tuple(to_srgb((1 - t) * to_linear(a) + t * to_linear(b)) for a, b in zip(rgb1, rgb2))
