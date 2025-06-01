import asyncio
from typing import Callable, List, Optional, Literal, Coroutine

from pydantic import Field
from model.instruction.instruction_base import AlphaInstruction

class AlphaStaticInstruction(AlphaInstruction):
    identifier: Literal["alpha_static"] = "alpha_static"
    alpha: float = Field(..., ge=0.0, le=1.0)

    def execute(self, current_alpha: List[float], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:        
        current_alpha.clear()
        current_alpha.extend([self.alpha] * led_count)
        redraw(None)
