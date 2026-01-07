from pydantic import Field
from ..command_base import CommandBase
from ...renderer.blender import BlendMode

class CommandSourceBase(CommandBase):
    blend: BlendMode = Field(default=BlendMode.NORMAL)