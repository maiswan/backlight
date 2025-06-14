from typing import Iterable, List, Literal
from pydantic import Field
from model.instruction.instruction import InstructionBase
from utilities.hsv2rgb import hsv2rgb

class ColorStaticHsvInstruction(InstructionBase):
    identifier: Literal["color_static_hsv"] = "color_static_hsv"
    hue: int = Field(..., ge=0, le=360)
    saturation: float = Field(..., ge=0, le=1)
    value: float = Field(..., ge=0, le=1)

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        red, green, blue = hsv2rgb(self.hue, self.saturation, self.value)

        for i in targets:
            current_red[i] = red
            current_green[i] = green
            current_blue[i] = blue

    
