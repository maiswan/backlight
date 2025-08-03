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
    config_path: str = ""
    current_red: list[float] = []
    current_green: list[float] = []
    current_blue: list[float] = []
    render_task: Task
    is_rendering: bool = False
    stop_event = Event()
    pixels: NeoPixel

    def initialize_render_task(self):
        if (self.is_rendering):
            return
        
        self.render_task = asyncio.create_task(self.render_loop())
        
    async def render_loop(self):
        self.is_rendering = True
        while True:
            now = time.monotonic()
            self.current_red = [0] * self.config.led_count
            self.current_green = [0] * self.config.led_count
            self.current_blue = [0] * self.config.led_count

            is_static = True
            self.config.commands.sort(key=lambda x: x.z_index)
            for command in self.config.commands:
                is_static = is_static and command.is_static
                command.execute(self.current_red, self.current_green, self.current_blue, self.config.led_count, now)
            
            self.redraw()

            # all commands are static, no need to rerender
            if (is_static or self.stop_event.is_set()):
                self.is_rendering = False
                self.render_task = None
                break

            await asyncio.sleep(1 / self.config.fps)

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
            pixel_order=read['pixel_order'],
            gpio_pin=read['gpio_pin'],
            fps=read['fps'],
            commands=read['commands'],
        )

        self.initialize_pixels()
        self.initialize_render_task()

        self.pixels.brightness = 1.0

    def initialize_pixels(self):
        self.pixels = NeoPixel(
            Pin(self.config.gpio_pin),
            self.config.led_count,
            auto_write=False,
            pixel_order=self.config.pixel_order,
        )

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