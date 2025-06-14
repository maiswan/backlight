from typing import Annotated, Union

from pydantic import Field
from .AlphaPulseInstruction import AlphaPulseInstruction
from .AlphaStaticInstruction import AlphaStaticInstruction
from .AlphaRollingInstruction import AlphaRollingInstruction

__all__ = ["AlphaPulseInstruction", "AlphaStaticInstruction", "AlphaRollingInstruction"]

# Discriminated unions
AlphaInstructionUnion = Annotated[
    Union[AlphaPulseInstruction, AlphaStaticInstruction, AlphaRollingInstruction],
    Field(discriminator="identifier")
]
