from typing import Iterable, List, Literal
from pydantic import Field, model_validator
from ..command_base import CommandBase

class CommandTransformMatrix(CommandBase):
    mode: Literal["transform_matrix"] = "transform_matrix"
    m11: float = Field(ge=-5.0, le=5.0, default=1.0)
    m12: float = Field(ge=-5.0, le=5.0, default=0.0)
    m13: float = Field(ge=-5.0, le=5.0, default=0.0)
    m21: float = Field(ge=-5.0, le=5.0, default=0.0)
    m22: float = Field(ge=-5.0, le=5.0, default=1.0)
    m23: float = Field(ge=-5.0, le=5.0, default=0.0)
    m31: float = Field(ge=-5.0, le=5.0, default=0.0)
    m32: float = Field(ge=-5.0, le=5.0, default=0.0)
    m33: float = Field(ge=-5.0, le=5.0, default=1.0)
    bias_red: float = Field(ge=-255.0, le=255.0, default=0.0)
    bias_green: float = Field(ge=-255.0, le=255.0, default=0.0)
    bias_blue: float = Field(ge=-255.0, le=255.0, default=0.0)
    is_static = True

    def _compute(self, buffer: List[tuple[float, float, float]], targets: Iterable[int], time: float):
        br = self.bias_red / 255
        bg = self.bias_green / 255
        bb = self.bias_blue / 255

        for i in targets:
            old_r = buffer[i][0]
            old_g = buffer[i][1]
            old_b = buffer[i][2]

            r = (old_r * self.m11) + (old_g * self.m12) + (old_b * self.m13) + br
            g = (old_r * self.m21) + (old_g * self.m22) + (old_b * self.m23) + bg
            b = (old_r * self.m31) + (old_g * self.m32) + (old_b * self.m33) + bb

            buffer[i] = (r, g, b)
