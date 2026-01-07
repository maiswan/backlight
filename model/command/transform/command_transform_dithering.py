from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from ..command_base import CommandBase

class CommandTransformDithering(CommandBase):
    mode: Literal["transform_dithering"] = "transform_dithering"
    min_red: int = Field(ge=1, default=1)
    min_green: int = Field(ge=1, default=1)
    min_blue: int = Field(ge=1, default=1)
    is_static = True

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        threshold_red = self.min_red / 255
        threshold_green = self.min_green / 255
        threshold_blue = self.min_blue / 255

        error_red = 0
        error_green = 0
        error_blue = 0

        for i in targets:
            old_red = buffer[i][0]
            old_green = buffer[i][1]
            old_blue = buffer[i][2]

            error_red += old_red - round(old_red * 255) / 255
            error_green += old_green - round(old_green * 255) / 255
            error_blue += old_blue - round(old_blue * 255) / 255

            # propagate error to the next target
            next_index = next(targets)

            new_red = old_red
            new_green = old_green
            new_blue = old_blue
            has_propagated = False
            
            if (error_red >= threshold_red):
                new_red = buffer[next_index][0] + error_red
                has_propagated = True
                error_red = 0
                
            if (error_green >= threshold_green):
                new_green = buffer[next_index][1] + error_green
                has_propagated = True
                error_green = 0

            if (error_blue >= threshold_blue):
                new_blue = buffer[next_index][2] + error_blue
                has_propagated = True
                error_blue = 0

            if (has_propagated):
                buffer[next_index] = (new_red, new_green, new_blue)
            
