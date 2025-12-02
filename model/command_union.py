from typing import Annotated, Union

from pydantic import Field
from .command.source.command_source_rgb import CommandSourceRgb

# Discriminated unions
CommandUnion = Annotated[
    Union[CommandSourceRgb],
    Field(discriminator="mode")
]