from pi5neo import Pi5Neo, EPixelType

from ..buffer_types import RgbTuple
from .denormalizer import Denormalizer
from .pixel_order import PixelOrder
from .pixel_base import PixelBase

class NeoPixelSPI(PixelBase):

    _pixels: Pi5Neo
    _has_white_channel: bool

    @property
    def pixels(self):
        return self._pixels

    def __getitem__(self, key):
        return None

    def __setitem__(self, key: int, value: RgbTuple):
        if self._has_white_channel:
            output = Denormalizer.toRgbwTuple(value)
            self._pixels.set_led_color(key, output[0], output[1], output[2], output[3])
            return

        output = Denormalizer.toRgbTuple(value)
        self._pixels.set_led_color(key, output[0], output[1], output[2])

    def __init__(self, device: str, speed_khz: int, count: int, pixel_order: PixelOrder):
        self._has_white_channel = "W" in pixel_order
        pixel_type = EPixelType(pixel_order)

        self._pixels = Pi5Neo(device, count, speed_khz, pixel_type, True)

    def show(self):
        self._pixels.update_strip(None)

    def clear(self):
        self._pixels.clear_strip()
        self.show()
