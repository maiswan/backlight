from typing import Annotated, Union
from pydantic import Field

from .command.source.command_source_rgb import CommandSourceRgb
from .command.source.command_source_hsv import CommandSourceHsv
from .command.source.command_source_kelvin import CommandSourceKelvin
from .command.source.command_source_rainbow import CommandSourceRainbow

from .command.transform.command_transform_gamma import CommandTransformGamma
from .command.transform.command_transform_brightness import CommandTransformBrightness
from .command.transform.command_transform_matrix import CommandTransformMatrix

# Discriminated unions
CommandUnion = Annotated[
    Union[
        CommandSourceRgb, CommandSourceHsv, CommandSourceKelvin, CommandSourceRainbow,
        CommandTransformGamma, CommandTransformBrightness, CommandTransformMatrix
    ],
    Field(discriminator="mode")
]