from typing import Annotated, Union

from pydantic import Field
from .AlphaPulseCommand import AlphaPulseCommand
from .AlphaStaticCommand import AlphaStaticCommand
from .AlphaRollingCommand import AlphaRollingCommand

__all__ = ["AlphaPulseCommand", "AlphaStaticCommand", "AlphaRollingCommand"]

# Discriminated unions
AlphaCommandUnion = Annotated[
    Union[AlphaPulseCommand, AlphaStaticCommand, AlphaRollingCommand],
    Field(discriminator="mode")
]
