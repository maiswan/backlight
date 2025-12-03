from typing import Annotated, Union

from pydantic import Field
from .command.source.command_source_rgb import CommandSourceRgb
from .command.source.command_source_hsv import CommandSourceHsv
from .command.source.command_source_kelvin import CommandSourceKelvin

# Discriminated unions
CommandUnion = Annotated[
    Union[CommandSourceRgb, CommandSourceHsv, CommandSourceKelvin],
    Field(discriminator="mode")
]