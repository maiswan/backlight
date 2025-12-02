from board import SPI
from neopixel_spi import NeoPixel_SPI
from .pixel_base import PixelBase

class NeoPixelSPI(PixelBase):

    _pixels: NeoPixel_SPI
    _resend_count: int

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
        for i in range(self._resend_count):
            self._pixels.brightness = value
            self._pixels.show()

    def __init__(self, pin: int, count: int, pixel_order: str, resend_count: int):
        spi = SPI()
        self._pixels = NeoPixel_SPI(
            spi,
            count,
            pixel_order=pixel_order,
            auto_write=False
        )
        self._resend_count = resend_count

    def show(self):
        for i in range(self._resend_count):
            self._pixels.show()
