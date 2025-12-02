from asyncio import Task
import asyncio
import json
import os
import time
from .pixels.pixel_base import PixelBase
from .config import Config

class State:
    config: Config
    config_path: str = ""
    buffer: list[tuple[float, float, float]] = []
    render_task: Task | None = None
    loop = asyncio.get_event_loop()
    pixels: PixelBase

    def initialize_render_task(self):
        if (self.render_task): self.render_task.cancel()        
        self.render_task = self.loop.create_task(self.render_loop())
                
    async def render_loop(self):
        self.config.commands.sort(key=lambda x: x.z_index)

        self.buffer = [(0.0, 0.0, 0.0)] * self.config.led_count

        for command in self.config.commands:
            buffer = [(0.0, 0.0, 0.0)] * self.config.led_count
            command.execute(buffer, self.config.led_count, 0)

            # lerp between layers
            for index in command.get_targets(self.config.led_count):
                r1, g1, b1 = self.buffer[index]
                r2, g2, b2 = buffer[index]
                a = command.alpha

                r = r1 * (1 - a) + r2 * a
                g = g1 * (1 - a) + g2 * a
                b = b1 * (1 - a) + b2 * a

                self.buffer[index] = (r, g, b)

        self.redraw()
        # while True:
        #     now = time.monotonic()
        #     self.current_red = [0] * self.config.led_count
        #     self.current_green = [0] * self.config.led_count
        #     self.current_blue = [0] * self.config.led_count
# 
        #     is_static = True
        #     self.config.commands.sort(key=lambda x: x.z_index)
        #     for command in self.config.commands:
        #         if (not command.is_enabled):
        #             continue
# 
        #         is_static = is_static and command.is_static
        #         try:
        #             command.execute(self.current_red, self.current_green, self.current_blue, self.config.led_count, now)
        #         except Exception as exception:
        #             print(exception)
        #     
        #     self.redraw()
# 
        #     # all commands are static, no need to rerender
        #     if (is_static and self.config.fps_all_static_commands == 0):
        #         self.render_task = None
        #         break
# 
        #     fps = self.config.fps_all_static_commands if is_static else self.config.fps
        #     await asyncio.sleep(1 / fps)

    def toRgbwTuple(self, tuple: tuple[float, float, float]):
        white = min(tuple[0], tuple[1], tuple[2])
        return (tuple[0] - white, tuple[1] - white, tuple[2] - white, white)

    def redraw(self):
        need_rgbw_conversion = "W" in self.config.pixel_order

        for i in range(self.config.led_count):
            pixel = self.toRgbwTuple(self.buffer[i]) if need_rgbw_conversion else self.buffer[i]
            self.pixels[i] = pixel
        self.pixels.show()

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
            use_spi=read['use_spi'],
            spi_resend_count=read['spi_resend_count'],
            gpio_pin=read['gpio_pin'],
            fps=read['fps'],
            fps_all_static_commands=read['fps_all_static_commands'],
            commands=read['commands'],
        )

        self.initialize_pixels()
        self.initialize_render_task()

        self.pixels.brightness = 1.0

    def initialize_pixels(self):
        if (self.config.use_spi):
            from .pixels.spi import NeoPixelSPI
            self.pixels = NeoPixelSPI(
                self.config.gpio_pin,
                self.config.led_count,
                self.config.pixel_order,
                self.config.spi_resend_count
            )
            return
            
        from .pixels.gpio import NeoPixelGPIO
        self.pixels = NeoPixelGPIO(
            self.config.gpio_pin,
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