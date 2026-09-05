from typing import Annotated, Union
from pydantic import Field

from .source.command_source_rgb import CommandSourceRgb
from .source.command_source_hsv import CommandSourceHsv
from .source.command_source_kelvin import CommandSourceKelvin
from .source.command_source_rainbow import CommandSourceRainbow
from .source.command_source_rainbow_rolling import CommandSourceRainbowRolling

from .transform.command_transform_gamma import CommandTransformGamma
from .transform.command_transform_brightness import CommandTransformBrightness
from .transform.command_transform_brightness_breathing import CommandTransformBrightnessBreathing
from .transform.command_transform_brightness_rolling import CommandTransformBrightnessRolling
from .transform.command_transform_matrix import CommandTransformMatrix
from .transform.command_transform_dithering import CommandTransformDithering

# Discriminated unions
CommandUnion = Annotated[
    Union[
        CommandSourceRgb, CommandSourceHsv, CommandSourceKelvin, CommandSourceRainbow, CommandSourceRainbowRolling,
        CommandTransformGamma, CommandTransformBrightness, CommandTransformBrightnessBreathing, CommandTransformBrightnessRolling, CommandTransformMatrix, CommandTransformDithering
    ],
    Field(discriminator="mode")
]