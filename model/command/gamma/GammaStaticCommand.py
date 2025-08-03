from typing import Iterable, List, Literal
from pydantic import Field
from model.command.command import CommandBase

class GammaStaticCommand(CommandBase):
    mode: Literal["gamma_static"] = "gamma_static"
    gamma: float = Field(..., ge=0.1, le=5.0)
    is_static = True

    def _compute(self, current_red: List[float], current_green: List[float], current_blue: List[float], targets: Iterable[int], time: float):
        for i in targets:
            current_red[i] = (current_red[i]/255) ** self.gamma * 255
            current_green[i] = (current_green[i]/255) ** self.gamma * 255
            current_blue[i] = (current_blue[i]/255) ** self.gamma * 255
    
