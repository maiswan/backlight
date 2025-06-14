from typing import Iterable, List, Literal
from pydantic import Field
from model.instruction.instruction import InstructionBase
from utilities.kelvin2rgb import kelvin2rgb

class ColorStaticKelvinInstruction(InstructionBase):
    identifier: Literal["color_static_kelvin"] = "color_static_kelvin"
    kelvin: int = Field(..., ge=1000, le=12000)

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        red, green, blue = kelvin2rgb(self.kelvin)

        for i in targets:
            current_red[i] = red
            current_green[i] = green
            current_blue[i] = blue
