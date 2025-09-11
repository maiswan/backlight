from typing import Iterable, List, Literal
from pydantic import Field
from model.command.command import CommandBase
from utilities.hsv2rgb import hsv2rgb

class ColorRainbowCommand(CommandBase):
    mode: Literal["color_rainbow"] = "color_rainbow"
    period: float = Field(..., ge=1000)
    saturation: float = Field(..., ge=0.0, le=1.0)
    is_static = False

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        hue = (time * 1000 % self.period) / self.period * 360
        red, green, blue = hsv2rgb(hue, self.saturation, 1.0)

        for i in targets:
            current_red[i] = red
            current_green[i] = green
            current_blue[i] = blue
    
