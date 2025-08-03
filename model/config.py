# from typing import Union
from typing import Annotated, Union
from pydantic import BaseModel, Field

from model.command.alpha import AlphaCommandUnion
from model.command.color import ColorCommandUnion
from model.command.gamma import GammaCommandUnion

commandUnion = Annotated[
    Union[AlphaCommandUnion, ColorCommandUnion, GammaCommandUnion],
    Field(discriminator="mode")
]

# Main config model
class Config(BaseModel):
    led_count: int
    pixel_order: str
    gpio_pin: int
    fps: int
    commands: list[commandUnion] = []

    def to_dict(self):
        return {
            'led_count': self.led_count,
            'pixel_order': self.pixel_order,
            'gpio_pin': self.gpio_pin,
            'fps': self.fps,
            'commands': [instr.model_dump(mode='json') for instr in self.commands],
        }