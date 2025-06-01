import asyncio
from typing import Callable, List, Optional, Literal, Coroutine

from pydantic import Field
from model.instruction.instruction_base import ColorInstruction
from utilities.kelvin2rgb import kelvin2rgb

class ColorStaticKelvinInstruction(ColorInstruction):
    identifier: Literal["color_static_kelvin"] = "color_static_kelvin"
    kelvin: int = Field(..., ge=1000, le=12000)
    
    def execute(self, current_red: List[int], current_green: List[int], current_blue: List[int], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:
        red, green, blue = kelvin2rgb(self.kelvin)

        # Modify the lists in-place
        current_red.clear()
        current_red.extend([red] * led_count)
        
        current_green.clear()
        current_green.extend([green] * led_count)
        
        current_blue.clear()
        current_blue.extend([blue] * led_count)
        redraw(None)
