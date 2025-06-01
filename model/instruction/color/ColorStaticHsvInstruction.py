import asyncio
from typing import Callable, List, Optional, Literal, Coroutine

from pydantic import Field
from model.instruction.instruction_base import ColorInstruction
from utilities.hsv2rgb import hsv2rgb

class ColorStaticHsvInstruction(ColorInstruction):
    identifier: Literal["color_static_hsv"] = "color_static_hsv"
    hue: int = Field(..., ge=0, le=360)
    saturation: float = Field(..., ge=0, le=1)
    value: int = Field(..., ge=0, le=1)
    
    def execute(self, current_red: List[int], current_green: List[int], current_blue: List[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:
        red, green, blue = hsv2rgb(self.hue, self.saturation, self.value)

        # Modify the lists in-place
        current_red.clear()
        current_red.extend([red] * led_count)
        
        current_green.clear()
        current_green.extend([green] * led_count)
        
        current_blue.clear()
        current_blue.extend([blue] * led_count)
        redraw(None)
