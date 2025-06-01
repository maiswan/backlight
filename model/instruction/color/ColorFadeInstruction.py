import asyncio
import copy
import math
import time
from typing import Callable, Optional, Literal, Coroutine
from pydantic import Field
from model.instruction.instruction_base import ColorInstruction

class ColorFadeInstruction(ColorInstruction):
    identifier: Literal["color_fade"] = "color_fade"
    period_ms: int = Field(..., ge=0)
    red: int = Field(..., ge=0, le=255)
    green: int = Field(..., ge=0, le=255)
    blue: int = Field(..., ge=0, le=255)
    
    def execute(self, current_red: list[int], current_green: list[int], current_blue: list[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:
        return self.apply(self.period_ms, current_red, current_green, current_blue, led_count, redraw, stop)
    
    async def apply(self, period_ms: int, current_red: list[int], current_green: list[int], current_blue: list[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event):
        start_red = copy.deepcopy(current_red)
        start_green = copy.deepcopy(current_green)
        start_blue = copy.deepcopy(current_blue)
        start_time = time.time()

        percentage = 0.0
        while abs(percentage-1.0) > 0.0001 and not stop.is_set():
            linear_percentage = min(1.0, (time.time() - start_time) / (period_ms / 1000))
            eased_percentage = -1 * math.cos(math.pi * linear_percentage) / 2 + 0.5  # Cosine easing
            for i in range(led_count):
                red, green, blue = self.lerp_rgb(
                    (start_red[i], start_green[i], start_blue[i]),
                    (self.red, self.green, self.blue),
                    eased_percentage
                )
                current_red[i] = red
                current_green[i] = green
                current_blue[i] = blue
            redraw(None)
            await asyncio.sleep(0.01)  # yield control

    def lerp_rgb(self, rgb1: tuple[int, int, int], rgb2: tuple[int, int, int], t: float):
        to_linear = lambda c: (c / 255) ** 2.2
        to_srgb = lambda c: round((c ** (1 / 2.2)) * 255)
        return tuple(to_srgb((1 - t) * to_linear(a) + t * to_linear(b)) for a, b in zip(rgb1, rgb2))