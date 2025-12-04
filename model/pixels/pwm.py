from microcontroller import Pin
from neopixel import NeoPixel
from .pixel_base import PixelBase

class NeoPixelPWM(PixelBase):

    _pixels: NeoPixel

    @property
    def pixels(self):
        return self._pixels

    def __getitem__(self, key):
        return self._pixels[key]

    def __setitem__(self, key, value):
        self._pixels[key] = value

    @property
    def brightness(self):
        return self._pixels._brightness

    @brightness.setter
    def brightness(self, value: float):
        self._pixels.brightness = value

    def __init__(self, pin: int, count: int, pixel_order: str):
        self._pixels = NeoPixel(
            Pin(pin),
            count,
            auto_write=False,
            pixel_order=pixel_order,
        )

    def show(self):
        self._pixels.show()
