from typing import Literal
from pydantic import BaseModel, Field

class PwmConfig(BaseModel):
    pin: int = Field(gt=0)

class SpiConfig(BaseModel):
    device: str
    speed_khz: int = Field(gt=0)

class TransportConfig(BaseModel):
    mode: Literal["pwm", "spi"]
    pwm: PwmConfig | None
    spi: SpiConfig | None

class LedConfig(BaseModel):
    count: int = Field(gt=0)
    pixel_order: str
    transport: TransportConfig
