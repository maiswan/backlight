from pi5neo import Pi5Neo, EPixelType
from .denormalizer import Denormalizer
from ..config.pixel_order import PixelOrder
from .pixel_base import PixelBase

class NeoPixelSPI(PixelBase):
    def __init__(self, device: str, speed_khz: int, led_count: int, pixel_order: PixelOrder):
        self._pixels = Pi5Neo(
            device,
            led_count,
            speed_khz,
            EPixelType(pixel_order),
            quiet_mode = True
        )
        self._has_white_channel = "W" in pixel_order

    def __enter__(self):
        self._pixels.__enter__()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.clear()
        return self._pixels.__exit__(exc_type, exc_value, traceback)

    def __getitem__(self, key):
        return self._pixels.get_led_color(key)

    def __setitem__(self, key, value):      
        if self._has_white_channel:
            output = Denormalizer.toRgbwTuple(value)
            self._pixels.set_led_color(key, output[0], output[1], output[2], output[3])
            return

        output = Denormalizer.toRgbTuple(value)
        self._pixels.set_led_color(key, output[0], output[1], output[2])

    def show(self):
        self._pixels.update_strip(None)
#
    def clear(self):
        self._pixels.clear_strip()
        self.show()
