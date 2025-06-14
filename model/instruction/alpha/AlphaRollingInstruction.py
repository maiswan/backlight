import asyncio
import math
import time
from typing import Callable, Iterable, List, Literal, ClassVar, Optional

from pydantic import Field, model_validator
from model.instruction.instruction import InstructionBase

class AlphaRollingInstruction(InstructionBase):
    identifier: Literal["alpha_rolling"] = "alpha_rolling"
    period_ms: int = Field(..., ge=1000)
    maximas: float = Field(..., ge=0.01)
    alpha_min: float = Field(..., ge=0.0, le=1.0)
    alpha_max: float = Field(..., ge=0.0, le=1.0)

    @model_validator(mode='after')
    def validate_alpha_range(self) -> 'AlphaRollingInstruction':
        if self.alpha_min >= self.alpha_max:
            raise ValueError("alpha_min must be less than alpha_max")
        return self

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        for i in targets:
            alpha = (math.sin(self.maximas * math.pi * i/sum(1 for target in targets) + math.pi * 2 * (time * 1000 % self.period_ms) / self.period_ms) + 1) / 2
            alpha = round(self.alpha_min + (self.alpha_max - self.alpha_min) * alpha, 3)
            current_red[i] = current_red[i] * alpha
            current_green[i] = current_green[i] * alpha
            current_blue[i] = current_blue[i] * alpha
