from board import SPI
from neopixel_spi import NeoPixel_SPI
from .pixel_base import PixelBase

class NeoPixelSPI(PixelBase):

    spi = SPI()
    _pixels: NeoPixel_SPI

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
        self._pixels = NeoPixel_SPI(
            self.spi,
            count,
            pixel_order=pixel_order,
            auto_write=False
        )

    def show(self):
        self._pixels.show()
