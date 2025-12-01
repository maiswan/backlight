from asyncio import Task
import asyncio
import json
import os
import time
from pixels.pixel_base import PixelBase
from .config import Config

class State:
    config: Config
    config_path: str = ""
    current_red: list[float] = []
    current_green: list[float] = []
    current_blue: list[float] = []
    render_task: Task | None = None
    force_rerender_task: Task | None = None
    loop = asyncio.get_event_loop()
    pixels: PixelBase

    def initialize_render_task(self):
        if (self.render_task): self.render_task.cancel()        
        self.render_task = self.loop.create_task(self.render_loop())

    def initialize_force_render_task(self):
        if (self.force_rerender_task): self.force_rerender_task.cancel()      
        self.force_rerender_task = self.loop.create_task(self.force_rerender_gpio_loop())
                
    async def render_loop(self):
        while True:
            now = time.monotonic()
            self.current_red = [0] * self.config.led_count
            self.current_green = [0] * self.config.led_count
            self.current_blue = [0] * self.config.led_count

            is_static = True
            self.config.commands.sort(key=lambda x: x.z_index)
            for command in self.config.commands:
                if (not command.is_enabled):
                    continue

                is_static = is_static and command.is_static
                try:
                    command.execute(self.current_red, self.current_green, self.current_blue, self.config.led_count, now)
                except Exception as exception:
                    print(exception)
            
            self.redraw()

            # all commands are static, no need to rerender
            if (is_static and self.config.fps_all_static_commands == 0):
                self.render_task = None
                break

            fps = self.config.fps_all_static_commands if is_static else self.config.fps
            await asyncio.sleep(1 / fps)

    def toRgbwTuple(self, red: int, green: int, blue: int):
        white = min(red, green, blue)
        return (red - white, green - white, blue - white, white)

    def redraw(self, index: int | None = None):
        need_rgbw_conversion = "W" in self.config.pixel_order

        output_range = range(self.config.led_count) if index is None else range(index, index + 1)

        for i in output_range:
            pixel_tuple = self.toRgbwTuple(self.current_red[i], self.current_green[i], self.current_blue[i]) if need_rgbw_conversion else (self.current_red[i], self.current_green[i], self.current_blue[i])
            self.pixels[i] = pixel_tuple
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
            gpio_pin=read['gpio_pin'],
            fps=read['fps'],
            fps_all_static_commands=read['fps_all_static_commands'],
            force_rerender_gpio_pin=read['force_rerender_gpio_pin'],
            commands=read['commands'],
        )

        self.initialize_pixels()
        self.initialize_render_task()
        self.initialize_force_render_task()

        self.pixels.brightness = 1.0

    async def force_rerender_gpio_loop(self):
        pass
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.config.force_rerender_gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # prev = 0
        # 
        # while True:
        #     current = GPIO.input(self.config.force_rerender_gpio_pin)
        #     if (prev != current and current == GPIO.HIGH):
        #         self.initialize_render_task()
# 
        #     prev = current
        #     await asyncio.sleep(1)

    def initialize_pixels(self):
        if (self.config.use_spi):
            from .pixels.spi import NeoPixelSPI
            self.pixels = NeoPixelSPI(
                self.config.gpio_pin,
                self.config.led_count,
                self.config.pixel_order,
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
        if (self.force_rerender_task): 
            self.force_rerender_task.cancel()
            await self.force_rerender_task

        self.write_config()


# Singleton instance
state: State = State()