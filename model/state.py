from asyncio import Task
import asyncio
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
        self.render_task = self.loop.create_task(self._render_loop())

    def _redraw(self, buffer: list[tuple[float, float, float]] | list[tuple[float, float, float, float]]):
        for i in range(self.config.led_count):
            self.pixels[i] = buffer[i]
        self.pixels.show()

    def _render(self, needs_rgbw: bool):
        return Renderer.render(
            self.config.commands,
            self.config.led_count,
            needs_rgbw
        )
                
    async def _render_loop(self):
        needs_rgbw = "W" in self.config.pixel_order  

        # First frame
        is_static, buffer = self._render(needs_rgbw)
        self._redraw(buffer)
        
        # Fast exit if the user doesn't want to rerender static content
        if (is_static and self.config.fps_static <= 0):
            return

        # Redraw every frame
        if is_static:
            # STATIC: no rerender, just redraw
            interval = 1.0 / self.config.fps_static
            while True:
                await asyncio.sleep(interval)
                self._redraw(buffer)
                
        # ANIMATED: rerender then redraw
        interval = 1.0 / self.config.fps
        while True:
            await asyncio.sleep(interval)
            _, buffer = self._render(needs_rgbw)
            self._redraw(buffer)

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
        config_path = self._get_config_path()
        self.config = Config.load(config_path)

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

    async def deconstruct(self):            
        # Turn off LEDs
        self.pixels.brightness = 0.0
        self.pixels.show()

        if (self.render_task): 
            self.render_task.cancel()
            await self.render_task

        self.config.write()


# Singleton instance
state: State = State()