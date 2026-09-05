from pydantic import Field
from ..command_base import CommandBase
from ...renderer import BlendMode

class CommandSourceBase(CommandBase):
    blend: BlendMode = Field(default=BlendMode.NORMAL)