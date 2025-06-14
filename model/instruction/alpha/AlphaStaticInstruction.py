from typing import Iterable, List, Literal
from pydantic import Field
from model.instruction.instruction import InstructionBase

class AlphaStaticInstruction(InstructionBase):
    identifier: Literal["alpha_static"] = "alpha_static"
    alpha: float = Field(..., ge=0.0, le=1.0)

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        for i in targets:
            current_red[i] *= self.alpha
            current_green[i] *= self.alpha
            current_blue[i] *= self.alpha
