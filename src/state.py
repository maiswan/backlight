from asyncio import get_event_loop, Task, sleep
from .config import Config
from .pixels import PixelBase, get_pixels
from .renderer import Renderer, Transitioner, RgbBuffer
from .time import DeterministicTimeSource, RealTimeSource

class State:

    def __init__(self):
        self.config = Config.load()
        self.buffer: RgbBuffer = [(0.0, 0.0, 0.0)] * self.config.leds.count
        self.render_task: Task | None = None
        self.pixels: PixelBase

    def __enter__(self):
        self.pixels = get_pixels(self.config.leds)
        self.pixels.__enter__()

        for command in self.config.commands:
            command.clear_target_cache()

        self.restart_rendering()
        return self

    def restart_rendering(self):
        if (self.render_task):
            self.render_task.cancel()
        loop = get_event_loop()
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
                await sleep(interval / 1000)

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
                await sleep(interval / 1000)
                
        # ANIMATED: rerender then redraw
        interval = int(1000 / config.framerate.active)
        while True:
            _, self.buffer = self._render(time.now())
            self._redraw()
            time.advance(interval)
            await sleep(interval / 1000)
