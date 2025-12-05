from typing import Annotated, Union
from pydantic import Field

from .command.source.command_source_rgb import CommandSourceRgb
from .command.source.command_source_hsv import CommandSourceHsv
from .command.source.command_source_kelvin import CommandSourceKelvin
from .command.source.command_source_rainbow import CommandSourceRainbow
from .command.source.command_source_rainbow_rolling import CommandSourceRainbowRolling

from .command.transform.command_transform_gamma import CommandTransformGamma
from .command.transform.command_transform_brightness import CommandTransformBrightness
from .command.transform.command_transform_brightness_breathing import CommandTransformBrightnessBreathing
from .command.transform.command_transform_brightness_rolling import CommandTransformBrightnessRolling
from .command.transform.command_transform_matrix import CommandTransformMatrix
from .command.transform.command_transform_dithering import CommandTransformDithering

# Discriminated unions
CommandUnion = Annotated[
    Union[
        CommandSourceRgb, CommandSourceHsv, CommandSourceKelvin, CommandSourceRainbow, CommandSourceRainbowRolling,
        CommandTransformGamma, CommandTransformBrightness, CommandTransformBrightnessBreathing, CommandTransformBrightnessRolling, CommandTransformMatrix, CommandTransformDithering
    ],
    Field(discriminator="mode")
]