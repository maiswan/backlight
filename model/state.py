from asyncio import Event, Task
import asyncio
import json
import os
import time
from .config import Config
from microcontroller import Pin
from neopixel import NeoPixel

class State:
    config: Config
    current_red: list[float] = []
    current_green: list[float] = []
    current_blue: list[float] = []
    config_path: str = ""
    render_task: Task
    stop_event = Event()
    pixels: NeoPixel

    async def render_loop(self):
        while not self.stop_event.is_set():
            now = time.monotonic()
            self.current_red = [0] * self.config.led_count
            self.current_green = [0] * self.config.led_count
            self.current_blue = [0] * self.config.led_count

            self.config.instructions.sort(key=lambda x: x.z_index)
            for instruction in self.config.instructions:
                instruction.execute(self.current_red, self.current_green, self.current_blue, self.config.led_count, now)
            
            self.redraw()
            await asyncio.sleep(1 / self.config.fps)

    def to_dict(self):
        return {
            'config': self.config.model_dump(),
            'current_red': self.current_red,
            'current_green': self.current_green,
            'current_blue': self.current_blue,
        }

    def redraw(self, index: int | None = None):
        if (index is None):
            for i in range(self.config.led_count):
                self.pixels[i] = (self.current_red[i], self.current_green[i], self.current_blue[i])
            self.pixels.show()
            return
        
        self.pixels[index] = (self.current_red[index], self.current_green[index], self.current_blue[index])
        self.pixels.show()

    def _get_config_path(self):
        CONFIG_PATHS = [
            'config.private.json',
            'config.json'
        ]

        for config_path in CONFIG_PATHS:
            if os.path.exists(config_path):
                return config_path
            
        raise Exception("No configuration file found") 

    def __init__(self):
        self.config_path = self._get_config_path()

        with open(self.config_path) as f:
            read = json.load(f)

        self.config = Config(
            led_count=read['led_count'],
            led_order=read['led_order'],
            gpio_pin=read['gpio_pin'],
            fps=read['fps'],
            instructions=read['instructions'],
        )

        self.pixels = NeoPixel(
            Pin(self.config.gpio_pin),
            self.config.led_count,
            auto_write=False,
            pixel_order=self.config.led_order,
        )

        self.render_task = asyncio.create_task(self.render_loop())
        self.pixels.brightness = 1.0

    async def deconstruct(self):
        # Turn off LEDs
        self.pixels.brightness = 0.0
        self.pixels.show()

        self.stop_event.set()
        await self.render_task

        # Write config
        with open(self.config_path, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=4)

# Singleton instance
state: State = State()