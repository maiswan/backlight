from ..renderer import RgbTuple
from microcontroller import Pin
from neopixel import NeoPixel
from .denormalizer import Denormalizer
from ..config.pixel_order import PixelOrder
from .pixel_base import PixelBase

class NeoPixelPWM(PixelBase):

    def __init__(self, pin: int, count: int, pixel_order: PixelOrder):
        self._has_white_channel = "W" in pixel_order
        self._count = count
    
        self._pixels = NeoPixel(
            Pin(pin),
            count,
            auto_write=False,
            pixel_order=pixel_order,
        )
        self._pixels.brightness = 1

    def __enter__(self):
        self._pixels.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return self._pixels.__exit__(exc_type, exc_value, traceback)

    def __getitem__(self, key):
        return self._pixels[key]

    def __setitem__(self, key: int, value: RgbTuple):
        denormalize = Denormalizer.toRgbwTuple if self._has_white_channel else Denormalizer.toRgbTuple
        self._pixels[key] = denormalize(value)
    
    def show(self):
        self._pixels.show()

    def clear(self):
        self._pixels.fill((0, 0, 0))
        self.show()

