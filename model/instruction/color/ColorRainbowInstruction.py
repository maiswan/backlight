import asyncio
import time
from typing import Callable, Optional, Literal, Coroutine

from pydantic import Field
from model.instruction.instruction_base import ColorInstruction
from utilities.hsv2rgb import hsv2rgb

class ColorRainbowInstruction(ColorInstruction):
    identifier: Literal["color_rainbow"] = "color_rainbow"
    period_ms: int = Field(..., ge=1000)
    saturation: float = Field(..., ge=0.0, le=1.0)

    def execute(self, current_red: list[int], current_green: list[int], current_blue: list[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:        
        return self.apply(self.period_ms, current_red, current_green, current_blue, led_count, redraw, stop)
    
    async def apply(self, period_ms: int, current_red: list[int], current_green: list[int], current_blue: list[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> None:
        start_time = time.time()
        while not stop.is_set():
            t = (time.time() - start_time) * 1000
            hue = (t % period_ms) / period_ms * 360
            red, green, blue = hsv2rgb(hue, self.saturation, 1.0)

            current_red.clear()
            current_red.extend([red] * led_count)
            current_green.clear()
            current_green.extend([green] * led_count)
            current_blue.clear()
            current_blue.extend([blue] * led_count)
            redraw(None)
            # print(current_alpha[0])
            # for i in range(led_count):
            #     current_alpha[i] = alpha

            await asyncio.sleep(0.01)  # yield control