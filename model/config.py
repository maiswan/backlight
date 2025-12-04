from typing import Union
from typing import Annotated, Union
from pydantic import BaseModel, Field
from .command_union import CommandUnion

class Config(BaseModel):
    led_count: int
    pixel_order: str
    spi_enabled: bool
    pwm_pin: int
    fps: int
    fps_static: int
    commands: list[CommandUnion] = []

    def to_dict(self):
        return {
            'led_count': self.led_count,
            'pixel_order': self.pixel_order,
            'spi_enabled': self.spi_enabled,
            'pwm_pin': self.pwm_pin,
            'fps': self.fps,
            'fps_static': self.fps_static,
            'commands': [instr.model_dump(mode='json') for instr in self.commands],
        }