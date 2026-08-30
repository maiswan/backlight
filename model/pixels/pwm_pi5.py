from ..buffer_types import RgbTuple
from microcontroller import Pin
import adafruit_pixelbuf
from adafruit_raspberry_pi5_neopixel_write import neopixel_write
from .denormalizer import Denormalizer
from .pixel_order import PixelOrder
from .pixel_base import PixelBase

# https://raw.githubusercontent.com/adafruit/Adafruit_Blinka_Raspberry_Pi5_Neopixel/refs/heads/main/examples/led_animation.py
class Pi5PixelBuf(adafruit_pixelbuf.PixelBuf):
    def __init__(self, pin, size, **kwargs):
        self._pin = pin
        super().__init__(size=size, **kwargs)

    def _transmit(self, buf):
        neopixel_write(self._pin, buf)

class NeoPixelPWMPi5(PixelBase):

    _buffer: Pi5PixelBuf
    _has_white_channel: bool
    _count: int

    @property
    def pixels(self):
        return None

    def __getitem__(self, key: int):
        return None

    def __setitem__(self, key: int, value: RgbTuple):
        denormalize = Denormalizer.toRgbwTuple if self._has_white_channel else Denormalizer.toRgbTuple
        self._buffer[key] = denormalize(value)

    def __init__(self, pin: int, count: int, pixel_order: PixelOrder):

        self._has_white_channel = "W" in pixel_order
        self._count = count
        self._pin = pin
        self._buffer = Pi5PixelBuf(pin, count, auto_write=False, byteorder=pixel_order)

    def show(self):
        self._buffer._transmit(self._pin, self._buffer)

    def clear(self):
        pass

