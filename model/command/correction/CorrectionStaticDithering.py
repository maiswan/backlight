from typing import Iterable, List, Literal
from pydantic import Field
from model.command.command import CommandBase

class CorrectionStaticDitheringCommand(CommandBase):
    mode: Literal["correction_static_dithering"] = "correction_static_dithering"
    is_static = True
    
    min_red: int = Field(..., ge=0)
    min_green: int = Field(..., ge=0)
    min_blue: int = Field(..., ge=0)

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        
        error_red = 0
        error_green = 0
        error_blue = 0

        for (i, _) in enumerate(targets):
            old_red = current_red[i]
            old_green = current_green[i]
            old_blue = current_blue[i]

            current_red[i] = round(old_red)
            current_green[i] = round(old_green)
            current_blue[i] = round(old_blue)

            error_red += old_red - current_red[i]
            error_green += old_green - current_green[i]
            error_blue += old_blue - current_blue[i]

            if (i == len(targets)-1):
                return

            # propagate error to the next target
            next_target_index = targets[i+1]
            
            if (error_red >= self.min_red):
                current_red[next_target_index] = self._clamp(current_red[next_target_index] + error_red)
                error_red = 0
                
            if (error_green >= self.min_green):
                current_green[next_target_index] = self._clamp(current_green[next_target_index] + error_green)
                error_green = 0

            if (error_blue >= self.min_blue):
                current_blue[next_target_index] = self._clamp(current_blue[next_target_index] + error_blue)
                error_blue = 0

    def _clamp(self, value: float, minimum: int = 0, maximum: int = 255):
        if (value < minimum): return minimum
        if (value > maximum): return maximum
        return value
    
