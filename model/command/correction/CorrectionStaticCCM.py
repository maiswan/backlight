from typing import Iterable, List, Literal
from pydantic import Field
from model.command.command import CommandBase

class CorrectionStaticCCMCommand(CommandBase):
    mode: Literal["correction_static_ccm"] = "correction_static_ccm"
    m11: float = Field(..., ge=-1.0, le=1.0)
    m12: float = Field(..., ge=-1.0, le=1.0)
    m13: float = Field(..., ge=-1.0, le=1.0)
    m21: float = Field(..., ge=-1.0, le=1.0)
    m22: float = Field(..., ge=-1.0, le=1.0)
    m23: float = Field(..., ge=-1.0, le=1.0)
    m31: float = Field(..., ge=-1.0, le=1.0)
    m32: float = Field(..., ge=-1.0, le=1.0)
    m33: float = Field(..., ge=-1.0, le=1.0)
    bias_red: float = Field(..., ge=-255.0, le=255.0)
    bias_green: float = Field(..., ge=-255.0, le=255.0)
    bias_blue: float = Field(..., ge=-255.0, le=255.0)
    
    is_static = True

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        for i in targets:
            old_red = current_red[i]
            old_green = current_green[i]
            old_blue = current_blue[i]

            # Matrix multiplication with bias
            red = self.m11 * old_red + self.m12 * old_green + self.m13 * old_blue + self.bias_red
            green = self.m21 * old_red + self.m22 * old_green + self.m23 * old_blue + self.bias_green
            blue = self.m31 * old_red + self.m32 * old_green + self.m33 * old_blue + self.bias_blue
            
            # Clamp
            red = self._clamp(red)
            green = self._clamp(green)
            blue = self._clamp(blue)

            # Writeback
            current_red[i] = red
            current_green[i] = green
            current_blue[i] = blue

    def _clamp(self, value: float, minimum: float = 0, maximum: float = 255):
        if value < minimum: return minimum
        if value > maximum: return maximum
        return value


