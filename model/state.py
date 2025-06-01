from asyncio import Event, Task, create_task
import json
from typing import Any, Dict
from model.instruction.instruction_base import ColorInstruction, AlphaInstruction, GammaInstruction, Instruction
from .config import Config
from microcontroller import Pin
from neopixel import NeoPixel

class State:
    config: Config
    current_red: list[int] = []
    current_green: list[int] = []
    current_blue: list[int] = []
    current_alpha: list[float] = []
    current_gamma: list[float] = [1.0] # only consider the first element; the list is a workaround for pass-by-reference
    stop_sse_event = Event()
    pixels: NeoPixel

    stop_events: dict[type, Event | None] = {
        ColorInstruction: None,
        AlphaInstruction: None,
        GammaInstruction: None,
    }
    tasks: dict[type, Task | None] = {
        ColorInstruction: None,
        AlphaInstruction: None,
        GammaInstruction: None,
    }
    
    async def execute_instruction(self, instruction: Instruction) -> bool:
        # Get base instruction type (Color/Alpha/Gamma)
        instruction_type = None
        for type in [ColorInstruction, AlphaInstruction, GammaInstruction]:
            if (isinstance(instruction, type)):
                instruction_type = type
                break
        else:
            return False
        
        # Gracefully stop existing task
        if (self.stop_events[instruction_type] is not None):
            self.stop_events[instruction_type].set() # type: ignore

        stop_event = Event()
        self.stop_events[instruction_type] = stop_event
        
        # Execute instruction-specific logic
        coroutine = None
        if (isinstance(instruction, ColorInstruction)):
            coroutine = instruction.execute(self.current_red, self.current_green, self.current_blue, self.config.led_count, self.redraw,  stop_event)
            self.config.color_instruction = instruction # type: ignore
        elif (isinstance(instruction, AlphaInstruction)):
            coroutine = instruction.execute(self.current_alpha, self.config.led_count, self.redraw, stop_event)
            self.config.alpha_instruction = instruction # type: ignore
        elif (isinstance(instruction, GammaInstruction)):
            coroutine = instruction.execute(self.current_gamma, self.redraw, stop_event)
            self.config.gamma_instruction = instruction # type: ignore
    
        if (coroutine is None):
            return True

        # New instruction is long-running: forcefully overwrite existing task
        existing_task = self.tasks[instruction_type]
        if (existing_task is not None):
            existing_task.cancel()
        self.tasks[instruction_type] = create_task(coroutine)
        
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            'config': self.config.model_dump(),
            'current_red': self.current_red,
            'current_green': self.current_green,
            'current_blue': self.current_blue,
            'current_alpha': self.current_alpha,
            'current_gamma': self.current_gamma[0]
        }

    def redraw(self, index: int | None = None):
        gamma = self.current_gamma[0] # consider first value only
        if (index is None):
            # Update all pixels
            for i in range(self.config.led_count):
                r = int((self.current_red[i] * self.current_alpha[i] / 255) ** gamma * 255)
                g = int((self.current_green[i] * self.current_alpha[i] / 255) ** gamma * 255)
                b = int((self.current_blue[i] * self.current_alpha[i] / 255) ** gamma * 255)
                self.pixels[i] = (r, g, b)
        else:
            # Update only the specified pixel
            r = int((self.current_red[index] * self.current_alpha[index] / 255) ** gamma * 255)
            g = int((self.current_green[index] * self.current_alpha[index] / 255) ** gamma * 255)
            b = int((self.current_blue[index] * self.current_alpha[index] / 255) ** gamma * 255)
            self.pixels[index] = (r, g, b)
        self.pixels.show()

    def __init__(self, filename: str):
        with open(filename) as f:
            read = json.load(f)

        self.config = Config(
            led_count=read['led_count'],
            led_order=read['led_order'],
            gpio_pin=read['gpio_pin'],
            color_instruction=read['color_instruction'],
            alpha_instruction=read['alpha_instruction'],
            gamma_instruction=read['gamma_instruction'],
        )

        self.current_red = [0] * self.config.led_count
        self.current_green = [0] * self.config.led_count
        self.current_blue = [0] * self.config.led_count
        self.current_alpha = [1.0] * self.config.led_count

        self.pixels = NeoPixel(
            Pin(self.config.gpio_pin),
            self.config.led_count,
            auto_write=False,
            pixel_order=self.config.led_order,
        )

# Singleton instance
state: State = State('config.json')