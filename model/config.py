from typing import Union
from typing import Annotated, Union
from pydantic import BaseModel, Field
from .command_union import CommandUnion

class Config(BaseModel):
    led_count: int
    pixel_order: str
    use_spi: bool
    spi_resend_count: int
    gpio_pin: int
    fps: int
    fps_all_static_commands: int
    commands: list[CommandUnion] = []

    def to_dict(self):
        return {
            'led_count': self.led_count,
            'pixel_order': self.pixel_order,
            'use_spi': self.use_spi,
            'spi_resend_count': self.spi_resend_count,
            'gpio_pin': self.gpio_pin,
            'fps': self.fps,
            'fps_all_static_commands': self.fps_all_static_commands,
            'commands': [instr.model_dump(mode='json') for instr in self.commands],
        }