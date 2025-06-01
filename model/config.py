from pydantic import BaseModel
from model.instruction.alpha import AlphaInstructionUnion
from model.instruction.color import ColorInstructionUnion
from model.instruction.gamma import GammaInstructionUnion

# Main config model
class Config(BaseModel):
    led_count: int
    led_order: str
    gpio_pin: int
    color_instruction: ColorInstructionUnion | None = None
    alpha_instruction: AlphaInstructionUnion | None = None
    gamma_instruction: GammaInstructionUnion | None = None

    def to_dict(self):
        return {
            'led_count': self.led_count,
            'led_order': self.led_order,
            'gpio_pin': self.gpio_pin,
            'color_instruction': self.color_instruction.model_dump() if self.color_instruction else None,
            'alpha_instruction': self.alpha_instruction.model_dump() if self.alpha_instruction else None,
            'gamma_instruction': self.gamma_instruction.model_dump() if self.gamma_instruction else None,
        }