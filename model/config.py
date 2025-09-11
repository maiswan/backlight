# from typing import Union
from typing import Annotated, Union
from pydantic import BaseModel, Field

from model.command.alpha import AlphaCommandUnion
from model.command.color import ColorCommandUnion
from model.command.correction import CorrectionCommandUnion

commandUnion = Annotated[
    Union[AlphaCommandUnion, ColorCommandUnion, CorrectionCommandUnion],
    Field(discriminator="mode")
]

# Main config model
class Config(BaseModel):
    led_count: int
    pixel_order: str
    gpio_pin: int
    fps: int
    fps_all_static_commands: int
    force_rerender_gpio_pin: int
    commands: list[commandUnion] = []

    def to_dict(self):
        return {
            'led_count': self.led_count,
            'pixel_order': self.pixel_order,
            'gpio_pin': self.gpio_pin,
            'fps': self.fps,
            'fps_all_static_commands': self.fps_all_static_commands,
            'force_rerender_gpio_pin': self.force_rerender_gpio_pin,
            'commands': [instr.model_dump(mode='json') for instr in self.commands],
        }