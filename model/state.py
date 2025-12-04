from asyncio import Task
import asyncio
import json
import os
import time
from .pixels.pixel_base import PixelBase
from .config import Config
from .renderer.renderer import Renderer

class State:
    config: Config
    config_path: str = ""
    render_task: Task | None = None
    loop = asyncio.get_event_loop()
    pixels: PixelBase

    def initialize_render_task(self):
        if (self.render_task): self.render_task.cancel()        
        self.render_task = self.loop.create_task(self.render_loop())
                
    async def render_loop(self):
        needs_rgbw_conversion = "W" in self.config.pixel_order
        while True:
            is_static, buffer = Renderer.render(
                self.config.commands,
                self.config.led_count,
                needs_rgbw_conversion
            )

            # Redraw
            for i in range(self.config.led_count):
                self.pixels[i] = buffer[i]
            self.pixels.show()

            # Decide whether we need to render the next frame as well
            if (is_static and self.config.fps_static == 0):
                return

            fps = self.config.fps_static if is_static else self.config.fps
            await asyncio.sleep(1 / fps)

    def _get_config_path(self):
        CONFIG_PATHS = [
            'config.dev.json',
            'config.prod.json',
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
            spi_enabled=read['spi_enabled'],
            pwm_pin=read['pwm_pin'],
            fps=read['fps'],
            fps_static=read['fps_static'],
            commands=read['commands'],
        )

        self.initialize_pixels()
        self.initialize_render_task()

        self.pixels.brightness = 1.0

    def initialize_pixels(self):
        if (self.config.spi_enabled):
            from .pixels.spi import NeoPixelSPI
            self.pixels = NeoPixelSPI(
                self.config.led_count,
                self.config.pixel_order
            )
            return
            
        from .pixels.pwm import NeoPixelPWM
        self.pixels = NeoPixelGPIO(
            self.config.pwm_pin,
            self.config.led_count,
            self.config.pixel_order,
        )

    def write_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=4)

    async def deconstruct(self):            
        # Turn off LEDs
        self.pixels.brightness = 0.0
        self.pixels.show()

        if (self.render_task): 
            self.render_task.cancel()
            await self.render_task

        self.write_config()


# Singleton instance
state: State = State()