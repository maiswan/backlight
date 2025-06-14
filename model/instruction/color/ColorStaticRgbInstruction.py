from typing import Iterable, List, Literal
from pydantic import Field
from model.instruction.instruction import InstructionBase

class ColorStaticRgbInstruction(InstructionBase):
    identifier: Literal["color_static_rgb"] = "color_static_rgb"
    red: int = Field(..., ge=0, le=255)
    green: int = Field(..., ge=0, le=255)
    blue: int = Field(..., ge=0, le=255)

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        for i in targets:
            current_red[i] = self.red
            current_green[i] = self.green
            current_blue[i] = self.blue
        
    
