from asyncio import Task
import asyncio
import os
import time
import math
from .pixels.pixel_base import PixelBase
from .config.config import Config
from .renderer.renderer import Renderer
from .renderer.transitioner import Transitioner, EasingMode

class State:
    config: Config
    render_task: Task | None = None
    pixels: PixelBase
    buffer: list[tuple[float, float, float]] | list[tuple[float, float, float, float]] | None = None

    def initialize_render_task(self):
        if (self.render_task): self.render_task.cancel()
        loop = asyncio.get_event_loop()
        self.render_task = loop.create_task(self._render_loop())

    def _redraw(self, buffer: list[tuple[float, float, float]] | list[tuple[float, float, float, float]]):
        self.pixels[:] = buffer
        self.pixels.show()

    def _render(self, needs_rgbw: bool):
        return Renderer.render(
            self.config.commands,
            self.config.leds.count,
            needs_rgbw
        )
                
    async def _render_loop(self):
        needs_rgbw = "W" in self.config.leds.pixel_order  
        config = self.config.renderer

        # Populate buffer if None
        is_static = False

        if self.buffer is None:
            is_static, self.buffer = self._render(needs_rgbw)

        # Transition
        if config.transitions.duration > 0:
            interval = 1 / config.framerate.active
            progress = 0
            old_buffer = self.buffer
            new_buffer = None
            start_time = time.monotonic()

            while progress < 1:
                progress = (time.monotonic() - start_time) / config.transitions.duration

                if not is_static or new_buffer is None:
                    _, new_buffer = self._render(needs_rgbw)
                    
                self.buffer = Transitioner.transit(old_buffer, new_buffer, progress, config.transitions.mode)
                
                self._redraw(self.buffer)
                await asyncio.sleep(interval)
        
        # Fast exit if the user doesn't want to rerender static content repeatedly
        if (is_static and config.framerate.idle <= 0):
            _, self.buffer = self._render(needs_rgbw)
            self._redraw(self.buffer)
            return
            
        # Redraw every frame
        if is_static:
            # STATIC: no rerender, just redraw
            interval = 1.0 / config.framerate.idle
            while True:
                await asyncio.sleep(interval)
                self._redraw(self.buffer)
                
        # ANIMATED: rerender then redraw
        interval = 1.0 / config.framerate.active
        while True:
            await asyncio.sleep(interval)
            _, self.buffer = self._render(needs_rgbw)
            self._redraw(self.buffer)

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
        if (self.config.leds.transport.mode == "spi"):
            from .pixels.spi import NeoPixelSPI
            self.pixels = NeoPixelSPI(
                self.config.leds.count,
                self.config.leds.pixel_order
            )
            return
            
        from .pixels.pwm import NeoPixelPWM
        self.pixels = NeoPixelGPIO(
            self.config.leds.transport.pwm.pwm_pin,
            self.config.leds.count,
            self.config.leds.pixel_order,
        )

    async def deconstruct(self):
        if (self.render_task): 
            self.render_task.cancel()
            await self.render_task
 
        # Turn off LEDs
        self.pixels.brightness = 0.0
        self.pixels.show()

        self.config.write()
