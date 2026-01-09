from typing import Annotated, Union
from pydantic import BaseModel, Field, PrivateAttr, ConfigDict
from .command_union import CommandUnion
import json

class Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    port: int = Field(gt=0)
    led_count: int = Field(gt=0)
    pixel_order: str
    spi_enabled: bool
    pwm_pin: int = Field(gt=0)
    fps: float = Field(gt=0)
    fps_static: float = Field(ge=0)          # 0 => don't redraw
    transition_duration: float = Field(ge=0) # 0 => no transition
    commands: list[CommandUnion]
    _path: str = PrivateAttr()

    @classmethod
    def load(cls, path: str):
        with open(path, 'r') as f:
            data = json.load(f)

        config = cls.model_validate(data)
        config._path = path
        return config

    def write(self, path: str | None = None):
        if path is None:
            path = self._path

        if path is None:
            raise ValueError("No path specified for writing config")

        model_dump = self.model_dump(mode='json')

        with open(path, 'w') as f:
            json.dump(model_dump, f, indent=4)
