import os
from pydantic import BaseModel, Field, ConfigDict

from ..command import CommandUnion
from .led_config import LedConfig
from .renderer_config import RendererConfig
from .server_config import ServerConfig
import json

CONFIG_PATHS = [
    'config.dev.json',
    'config.prod.json',
    'config.json'
]

class Config(BaseModel):

    model_config = ConfigDict(validate_assignment=True)

    server: ServerConfig = Field(default_factory=ServerConfig)
    leds: LedConfig = Field()
    renderer: RendererConfig = Field(default_factory=RendererConfig)
    commands: list[CommandUnion] = Field([])

    _path: str | None = None

    @classmethod
    def _find_first_available_path(cls):
        for config_path in CONFIG_PATHS:
            if os.path.exists(config_path):
                return config_path
            
        raise Exception("No configuration file found")

    @classmethod
    def load(cls, path: str | None = None):
        path = path or cls._find_first_available_path()

        with open(path, 'r') as f:
            data = json.load(f)

        config = cls.model_validate(data)
        config._path = path
        return config

    def write(self, path: str | None = None):

        path = path or self._path

        if path is None:
            raise ValueError("No path specified for writing config")

        dump = self.model_dump_json(exclude_unset=True, indent=4)
        with open(path, 'w') as f:
            f.write(dump) 
