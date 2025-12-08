from typing import Annotated, Union
from pydantic import BaseModel, Field, PrivateAttr
from .command_union import CommandUnion
import json


class Config(BaseModel):
    port: int
    led_count: int
    pixel_order: str
    spi_enabled: bool
    pwm_pin: int
    fps: int
    fps_static: int
    commands: list[CommandUnion] = []
    _path: str | None = PrivateAttr(default=None)

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
