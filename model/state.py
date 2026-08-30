from asyncio import Task
import asyncio
import os
from .pixels.pixel_base import PixelBase
from .config.config import Config
from .config.led_config import SpiTransport
from .renderer.renderer import Renderer
from .renderer.transitioner import Transitioner
from .buffer_types import RgbBuffer
from .time.time_source_base import TimeSourceBase
from .time.monotonic_time_source import MonotonicTimeSource

class State:
    config: Config
    render_task: Task | None = None
    pixels: PixelBase
    buffer: RgbBuffer | None = None
    time_source: TimeSourceBase = MonotonicTimeSource()

    def initialize_render_task(self):
        if (self.render_task): self.render_task.cancel()
        loop = asyncio.get_event_loop()
        self.render_task = loop.create_task(self._render_loop())

    def _redraw(self):
        if self.buffer is None:
            return

        for i in range(len(self.buffer)):
            if "W" in self.config.leds.pixel_order:
                self.pixels[i] = Renderer.toRgbwTuple(self.buffer[i])
            else:
                self.pixels[i] = Renderer.toRgbTuple(self.buffer[i])
        self.pixels.show()

    def _render(self):
        return Renderer.render(
            self.config.commands,
            self.config.leds.count,
            self.time_source.now()
        )
                
    async def _render_loop(self):
        config = self.config.renderer

        # Populate buffer if None
        is_static = False

        if self.buffer is None:
            self.buffer = [(0.0, 0.0, 0.0)] * self.config.leds.count

        # Transition
        if config.transitions.duration > 0:
            interval = int(1000 / config.framerate.active)
            progress = 0
            old_buffer = self.buffer[:]
            new_buffer = None
            start_time = self.time_source.now()
  
            while progress < 1:
                progress = (self.time_source.now() - start_time) / config.transitions.duration
                if not is_static or new_buffer is None:
                    is_static, new_buffer = self._render()
                
                self.buffer = Transitioner.transit(old_buffer, new_buffer, progress, config.transitions.mode)
                self._redraw()

                self.time_source.advance(interval)
                await asyncio.sleep(interval / 1000)

        # Fast exit if the user doesn't want to rerender static content repeatedly
        if (is_static and config.framerate.idle <= 0):
            _, self.buffer = self._render()
            self._redraw()
            return
            
        # Redraw every frame
        if is_static:
            # STATIC: no rerender, just redraw
            interval = int(1000 / config.framerate.idle)
            while True:
                self._redraw()
                await asyncio.sleep(interval / 1000)
                
        # ANIMATED: rerender then redraw
        interval = int(1000 / config.framerate.active)
        while True:
            _, self.buffer = self._render()
            self._redraw()
            self.time_source.advance(interval)
            await asyncio.sleep(interval / 1000)

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

    def initialize_output(self):
        self.buffer = None
        self._initialize_pixels()
        self.initialize_render_task()
        for command in self.config.commands:
            command.clear_target_cache()

    def _initialize_pixels(self):
        if isinstance(self.config.leds.transport, SpiTransport):
            from .pixels.spi import NeoPixelSPI
            self.pixels = NeoPixelSPI(
                self.config.leds.transport.device,
                self.config.leds.transport.speed_khz,
                self.config.leds.count,
                self.config.leds.pixel_order
            )
            return
            
        from .pixels.pwm import NeoPixelPWM
        self.pixels = NeoPixelPWM(
            self.config.leds.transport.pin,
            self.config.leds.count,
            self.config.leds.pixel_order,
        )
    
    def uninitialize_output(self):
        if (self.render_task): 
            self.render_task.cancel() 
            self.pixels.clear()

    def deconstruct(self):
        self.uninitialize_output()
        self.config.write()
