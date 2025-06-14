# from typing import Union
from typing import Annotated, Union
from pydantic import BaseModel, Field

from .instruction.instruction import InstructionBase
# from model.instruction.instruction import InstructionUnion
from model.instruction.alpha import AlphaInstructionUnion
from model.instruction.color import ColorInstructionUnion
from model.instruction.gamma import GammaInstructionUnion

instructionUnion = Annotated[
    Union[AlphaInstructionUnion, ColorInstructionUnion, GammaInstructionUnion],
    Field(discriminator="identifier")
]

# Main config model
class Config(BaseModel):
    led_count: int
    led_order: str
    gpio_pin: int
    fps: int
    instructions: list[instructionUnion] = []

    def to_dict(self):
        return {
            'led_count': self.led_count,
            'led_order': self.led_order,
            'gpio_pin': self.gpio_pin,
            'fps': self.fps,
            'instructions': [instr.model_dump(mode='json') for instr in self.instructions],
        }