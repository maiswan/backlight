from typing import Annotated, Literal
from pydantic import BaseModel, Field
from ..pixels.pixel_order import PixelOrder

class PwmTransport(BaseModel):
    mode: Literal["pwm"]
    pin: int = Field(gt=0)

class SpiTransport(BaseModel):
    mode: Literal["spi"]
    device: str = Field(default="/dev/spidev0.0")
    speed_khz: int = Field(gt=0)

Transport = Annotated[
    PwmTransport | SpiTransport,
    Field(discriminator="mode")
]

class LedConfig(BaseModel):
    count: int = Field(gt=0)
    pixel_order: PixelOrder = Field(...)
    transport: Transport
