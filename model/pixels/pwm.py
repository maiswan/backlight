from ..buffer_types import RgbTuple
from microcontroller import Pin
from neopixel import NeoPixel
from .denormalizer import Denormalizer
from .pixel_order import PixelOrder
from .pixel_base import PixelBase

class NeoPixelPWM(PixelBase):

    _pixels: NeoPixel
    _has_white_channel: bool
    _count: int

    @property
    def pixels(self):
        return self._pixels

    def __getitem__(self, key):
        return self._pixels[key]

    def __setitem__(self, key: int, value: RgbTuple):
        denormalize = Denormalizer.toRgbwTuple if self._has_white_channel else Denormalizer.toRgbTuple
        self._pixels[key] = denormalize(value)

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

    def show(self):
        self._pixels.show()

    def clear(self):
        value = (0, 0, 0)
        for i in range(self._count):
            self.__setitem__(i, value)
        self.show()

