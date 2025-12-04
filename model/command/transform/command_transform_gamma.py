from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from ..command_base import CommandBase

class CommandTransformGamma(CommandBase):
    mode: Literal["transform_gamma"] = "transform_gamma"
    gamma: float = Field(ge=0.1, le=5.0, default=2.2)
    is_static = True

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        for i in targets:
            r = pow(buffer[i][0], self.gamma)
            g = pow(buffer[i][1], self.gamma)
            b = pow(buffer[i][2], self.gamma)
            buffer[i] = (r, g, b)
        