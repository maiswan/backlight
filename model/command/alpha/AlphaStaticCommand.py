from typing import Iterable, List, Literal
from pydantic import Field
from model.command.command import CommandBase

class AlphaStaticCommand(CommandBase):
    mode: Literal["alpha_static"] = "alpha_static"
    alpha: float = Field(..., ge=0.0, le=1.0)
    is_static = True

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        for i in targets:
            current_red[i] *= self.alpha
            current_green[i] *= self.alpha
            current_blue[i] *= self.alpha
