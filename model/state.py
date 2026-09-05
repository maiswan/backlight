from asyncio import Task
import asyncio
from .pixels.pixel_base import PixelBase
from .config.config import Config
from .config.led_config import SpiTransport
from .renderer.renderer import Renderer
from .renderer.transitioner import Transitioner
from .buffer_types import RgbBuffer
from .time.deterministic_time_source import DeterministicTimeSource
from .time.real_time_source import RealTimeSource

class State:

    def __init__(self):
        self.config = Config.load()
        self.buffer: RgbBuffer = [(0.0, 0.0, 0.0)] * self.config.leds.count
        self.render_task: Task | None = None
        self.pixels: PixelBase

    def __enter__(self):
        self.pixels = self._get_pixels()
        self.pixels.__enter__()

        for command in self.config.commands:
            command.clear_target_cache()

        self.restart_rendering()
        return self
    
    def _get_pixels(self):
        if isinstance(self.config.leds.transport, SpiTransport):
            from .pixels.spi import NeoPixelSPI
            return NeoPixelSPI(
                self.config.leds.transport.device,
                self.config.leds.transport.speed_khz,
                self.config.leds.count,
                self.config.leds.pixel_order
            )

        from .pixels.pwm import NeoPixelPWM
        return NeoPixelPWM(
            self.config.leds.transport.pin,
            self.config.leds.count,
            self.config.leds.pixel_order,
        )

    def restart_rendering(self):
        if (self.render_task):
            self.render_task.cancel()
        loop = asyncio.get_event_loop()
        self.render_task = loop.create_task(self._render_loop())
                
    def __exit__(self, exc_type, exc_value, traceback):
        if (self.render_task): 
                    self.render_task.cancel() 

        if (self.pixels):
            self.pixels.clear()
            self.pixels.__exit__(exc_type, exc_value, traceback)

        self.config.write()

    def _redraw(self):
        if self.buffer is None:
            return

        for i in range(len(self.buffer)):
            self.pixels[i] = self.buffer[i]
        self.pixels.show()

    def _render(self, time: int):
        return Renderer.render(
            self.config.commands,
            self.config.leds.count,
            time
        )
                
    async def _render_loop(self):
        config = self.config.renderer
        time = RealTimeSource() if config.time.source == "real" else DeterministicTimeSource()
        is_static = False

        # Transition
        if config.transitions.duration > 0:
            interval = int(1000 / config.framerate.active)
            progress: float = 0
            old_buffer = self.buffer
            new_buffer = None
            start_time = time.now()
  
            while progress < 1:
                progress = (time.now() - start_time) / config.transitions.duration

                if not is_static or new_buffer is None:
                    is_static, new_buffer = self._render(time.now())
                
                self.buffer = Transitioner.transit(old_buffer, new_buffer, progress, config.transitions.mode)
                self._redraw()

                time.advance(interval)
                await asyncio.sleep(interval / 1000)

        # Fast exit if the user doesn't want to rerender static content repeatedly
        if (is_static and config.framerate.idle <= 0):
            _, self.buffer = self._render(time.now())
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
            _, self.buffer = self._render(time.now())
            self._redraw()
            time.advance(interval)
            await asyncio.sleep(interval / 1000)
