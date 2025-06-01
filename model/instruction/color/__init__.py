from typing import Annotated, Union
from pydantic import Field
from .ColorStaticRgbInstruction import ColorStaticRgbInstruction
from .ColorStaticHsvInstruction import ColorStaticHsvInstruction
from .ColorStaticKelvinInstruction import ColorStaticKelvinInstruction
from .ColorRainbowInstruction import ColorRainbowInstruction
from .ColorFadeInstruction import ColorFadeInstruction

__all__ = ["ColorStaticRgbInstruction", "ColorStaticHsvInstruction", "ColorStaticKelvinInstruction", "ColorRainbowInstruction", "ColorFadeInstruction"]

# Discriminated union
ColorInstructionUnion = Annotated[
    Union[ColorStaticRgbInstruction, ColorStaticHsvInstruction, ColorStaticKelvinInstruction, ColorFadeInstruction, ColorRainbowInstruction],
    Field(discriminator="identifier")
]