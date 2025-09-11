from typing import Annotated, Union

from pydantic import Field
from .CorrectionStaticGamma import CorrectionStaticGammaCommand
from .CorrectionStaticCCM import CorrectionStaticCCMCommand
from .CorrectionStaticDithering import CorrectionStaticDitheringCommand

__all__ = ["CorrectionStaticGammaCommand", "CorrectionStaticCCMCommand", "CorrectionStaticDitheringCommand"]

# Discriminated unions
CorrectionCommandUnion = Annotated[
    Union[CorrectionStaticGammaCommand, CorrectionStaticCCMCommand, CorrectionStaticDitheringCommand],
    Field(discriminator="mode")
]
