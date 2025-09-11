from typing import Iterable, List, Literal
from pydantic import Field
from model.command.command import CommandBase

class ColorStaticRgbCommand(CommandBase):
    mode: Literal["color_static_rgb"] = "color_static_rgb"
    red: float = Field(..., ge=0, le=255)
    green: float = Field(..., ge=0, le=255)
    blue: float = Field(..., ge=0, le=255)
    is_static = True

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        for i in targets:
            current_red[i] = self.red
            current_green[i] = self.green
            current_blue[i] = self.blue
        
    
