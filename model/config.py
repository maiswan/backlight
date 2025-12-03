from typing import Union
from typing import Annotated, Union
from pydantic import BaseModel, Field
from .command_union import CommandUnion

class Config(BaseModel):
    led_count: int
    pixel_order: str
    spi_enabled: bool
    spi_resend_count: int
    spi_resend_sleep: float
    gpio_pin: int
    fps: int
    fps_all_static_commands: int
    commands: list[CommandUnion] = []

    def to_dict(self):
        return {
            'led_count': self.led_count,
            'pixel_order': self.pixel_order,
            'spi_enabled': self.spi_enabled,
            'spi_resend_count': self.spi_resend_count,
            'spi_resend_sleep': self.spi_resend_sleep,
            'gpio_pin': self.gpio_pin,
            'fps': self.fps,
            'fps_all_static_commands': self.fps_all_static_commands,
            'commands': [instr.model_dump(mode='json') for instr in self.commands],
        }