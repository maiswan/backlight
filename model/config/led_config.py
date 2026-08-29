from typing import Annotated, Literal
from pydantic import BaseModel, Field

class PwmTransport(BaseModel):
    mode: Literal["pwm"]
    pin: int = Field(gt=0)

class SpiTransport(BaseModel):
    mode: Literal["spi"]
    device: str
    speed_khz: int = Field(gt=0)

Transport = Annotated[
    PwmTransport | SpiTransport,
    Field(discriminator="mode")
]

class LedConfig(BaseModel):
    count: int = Field(gt=0)
    pixel_order: str
    transport: Transport
