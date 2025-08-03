from typing import Annotated, Union
from pydantic import Field
from .ColorStaticRgbCommand import ColorStaticRgbCommand
from .ColorStaticHsvCommand import ColorStaticHsvCommand
from .ColorStaticKelvinCommand import ColorStaticKelvinCommand
from .ColorRainbowCommand import ColorRainbowCommand
from .ColorFadeCommand import ColorFadeCommand

__all__ = ["ColorStaticRgbCommand", "ColorStaticHsvCommand", "ColorStaticKelvinCommand", "ColorRainbowCommand", "ColorFadeCommand"]

# Discriminated union
ColorCommandUnion = Annotated[
    Union[ColorStaticRgbCommand, ColorStaticHsvCommand, ColorStaticKelvinCommand, ColorFadeCommand, ColorRainbowCommand],
    Field(discriminator="mode")
]