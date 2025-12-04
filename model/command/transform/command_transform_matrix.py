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
        for i in targets:
            old_r = buffer[i][0]
            old_g = buffer[i][1]
            old_b = buffer[i][2]

            r = (old_r * self.m11) + (old_g * self.m12) + (old_b * self.m13) + self.bias_red
            g = (old_r * self.m21) + (old_g * self.m22) + (old_b * self.m23) + self.bias_red
            b = (old_r * self.m31) + (old_g * self.m32) + (old_b * self.m33) + self.bias_red

            r = self._clamp(r)
            g = self._clamp(g)
            b = self._clamp(b)

            buffer[i] = (r, g, b)

    def _clamp(self, value: float, minimum: float = 0, maximum: float = 255):
        if value < minimum: return minimum
        if value > maximum: return maximum
        return value
        