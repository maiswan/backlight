from typing import Annotated, Union

from pydantic import Field
from .GammaStaticCommand import GammaStaticCommand

__all__ = ["GammaStaticCommand"]

# Discriminated unions
GammaCommandUnion = Annotated[
    Union[GammaStaticCommand],
    Field(discriminator="mode")
]
