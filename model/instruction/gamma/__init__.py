from typing import Annotated, Union

from pydantic import Field
from .GammaStaticInstruction import GammaStaticInstruction

__all__ = ["GammaStaticInstruction"]

# Discriminated unions
GammaInstructionUnion = Annotated[
    Union[GammaStaticInstruction],
    Field(discriminator="identifier")
]
