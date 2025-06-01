import asyncio
from typing import Callable, List, Optional, Literal, Coroutine

from pydantic import Field
from model.instruction.instruction_base import GammaInstruction

class GammaStaticInstruction(GammaInstruction):
    identifier: Literal["gamma_static"] = "gamma_static"
    gamma: float = Field(..., ge=0.1, le=5.0)

    def execute(self, current_gamma: List[float], redraw: Callable[[Optional[int]], None], stop: asyncio.Event) -> Coroutine | None:
        current_gamma[0] = self.gamma
        redraw(None)
