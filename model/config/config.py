from typing import Annotated, Union
from pydantic import BaseModel, Field, PrivateAttr, ConfigDict
from ..command_union import CommandUnion
from .led_config import LedConfig
from .renderer_config import RendererConfig
from .server_config import ServerConfig
import json

class Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    server: ServerConfig
    leds: LedConfig
    renderer: RendererConfig
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
