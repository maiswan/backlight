from pydantic import BaseModel, Field, PrivateAttr, ConfigDict
from ..command_union import CommandUnion
from .led_config import LedConfig
from .renderer_config import RendererConfig
from .server_config import ServerConfig
import json

class Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    server: ServerConfig = Field(default_factory=ServerConfig)
    leds: LedConfig = Field()
    renderer: RendererConfig = Field(default_factory=RendererConfig)
    commands: list[CommandUnion] = Field(default=[])

    _path: str = PrivateAttr()

    @classmethod
    def load(cls, path: str):
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
