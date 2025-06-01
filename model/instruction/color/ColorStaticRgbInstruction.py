import asyncio
from typing import Callable, List, Optional, Literal, Coroutine

from pydantic import Field
from model.instruction.instruction_base import ColorInstruction

class ColorStaticRgbInstruction(ColorInstruction):
    identifier: Literal["color_static_rgb"] = "color_static_rgb"
    red: int = Field(..., ge=0, le=255)
    green: int = Field(..., ge=0, le=255)
    blue: int = Field(..., ge=0, le=255)
    
    def execute(self, current_red: List[int], current_green: List[int], current_blue: List[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:        
        # Modify the lists in-place
        current_red.clear()
        current_red.extend([self.red] * led_count)
        
        current_green.clear()
        current_green.extend([self.green] * led_count)
        
        current_blue.clear()
        current_blue.extend([self.blue] * led_count)
        redraw(None)
