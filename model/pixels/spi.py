from pi5neo import Pi5Neo
from pi5neo.pi5neo import EPixelType
from .pixel_base import PixelBase
import time

class NeoPixelSPI(PixelBase):

    _pixels: Pi5Neo
    _has_white_channel: bool
    _count: int

    @property
    def pixels(self):
        return self._pixels

    def __getitem__(self, key):
        return None

    def __setitem__(self, key, value):
        if self._has_white_channel:
            r = int(value[0])
            g = int(value[1])
            b = int(value[2])
            w = int(value[3])
            self._pixels.set_led_color(key, r, g, b, w)
            return

        r = int(value[0])
        g = int(value[1])
        b = int(value[2])
        self._pixels.set_led_color(key, r, g, b)

    def __init__(self, device: str, speed_khz: int, count: int, pixel_order: str):
        self._has_white_channel = "W" in pixel_order
        pixel_type = EPixelType.RGBW if self._has_white_channel else EPixelType.RGB

        self._pixels = Pi5Neo(device, count, speed_khz, pixel_type, True)
        self._count = count

    def show(self):
        self._pixels.update_strip(None)

    def clear(self):
        self._pixels.clear_strip()
        self.show()
