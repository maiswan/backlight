from typing import Annotated, Union

from pydantic import Field
from .CorrectionStaticGamma import CorrectionStaticGammaCommand
from .CorrectionStaticCCM import CorrectionStaticCCMCommand

__all__ = ["CorrectionStaticGammaCommand", "CorrectionStaticCCMCommand"]

# Discriminated unions
CorrectionCommandUnion = Annotated[
    Union[CorrectionStaticGammaCommand, CorrectionStaticCCMCommand],
    Field(discriminator="mode")
]
