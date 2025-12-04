from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from ..command_base import CommandBase

class CommandTransformGamma(CommandBase):
    mode: Literal["transform_gamma"] = "transform_gamma"
    gamma: float = Field(ge=0.1, le=5.0, default=2.2)
    is_static = True

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        for i in targets:
            r = pow(buffer[i][0] / 255.0, self.gamma) * 255.0
            g = pow(buffer[i][1] / 255.0, self.gamma) * 255.0
            b = pow(buffer[i][2] / 255.0, self.gamma) * 255.0
            buffer[i] = (r, g, b)
        