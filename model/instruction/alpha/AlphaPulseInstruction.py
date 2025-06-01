import asyncio
import math
import time
from typing import Callable, Optional, Literal, Coroutine

from pydantic import Field, model_validator
from model.instruction.instruction_base import AlphaInstruction

class AlphaPulseInstruction(AlphaInstruction):
    identifier: Literal["alpha_pulse"] = "alpha_pulse"
    period_ms: int = Field(..., ge=1000)
    alpha_min: float = Field(..., ge=0.0, le=1.0)
    alpha_max: float = Field(..., ge=0.0, le=1.0)

    @model_validator(mode='after')
    def validate_alpha_range(self) -> 'AlphaPulseInstruction':
        if self.alpha_min >= self.alpha_max:
            raise ValueError("alpha_min must be less than alpha_max")
        return self
    
    def execute(self, current_alpha: list[float], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:        
        return self.apply(self.period_ms, self.alpha_min, self.alpha_max, current_alpha, led_count, redraw, stop)
    
    async def apply(self, period_ms: int, alpha_min: float, alpha_max: float, current_alpha: list[float], led_count: int, redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> None:
        start_time = time.time()
        while not stop.is_set():
            t = (time.time() - start_time) * 1000
            alpha = (math.sin(2 * math.pi * (t % period_ms) / period_ms) + 1) / 2
            alpha = round(alpha_min + (alpha_max - alpha_min) * alpha, 3)
            
            current_alpha.clear()
            current_alpha.extend([alpha] * led_count)
            redraw(None)            

            await asyncio.sleep(0.01)  # yield control