import math
from typing import Iterable, List, Literal

from pydantic import Field, model_validator
from model.command.command import CommandBase

class AlphaPulseCommand(CommandBase):
    mode: Literal["alpha_pulse"] = "alpha_pulse"
    period: float = Field(..., ge=1000)
    alpha_min: float = Field(..., ge=0.0, le=1.0)
    alpha_max: float = Field(..., ge=0.0, le=1.0)
    is_static = False

    @model_validator(mode='after')
    def validate_alpha_range(self) -> 'AlphaPulseCommand':
        if self.alpha_min >= self.alpha_max:
            raise ValueError("alpha_min must be less than alpha_max")
        return self

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        alpha = (math.sin(2 * math.pi * (time * 1000 % self.period) / self.period) + 1) / 2
        alpha = round(self.alpha_min + (self.alpha_max - self.alpha_min) * alpha, 3)
            
        for i in targets:
            current_red[i] *= alpha
            current_green[i] *= alpha
            current_blue[i] *= alpha
    
