import time
from board import SPI
import neopixel_spi as neopixel
import random

NUM_PIXELS = 144
PIXEL_ORDER = neopixel.GRBW

spi = SPI()
# while not spi.try_lock():
#     pass
# spi.configure(baudrate=2400000)
# spi.unlock()

pixels = neopixel.NeoPixel_SPI(spi,
                               NUM_PIXELS,
                               pixel_order=PIXEL_ORDER,
                               auto_write=False)

for i in range(NUM_PIXELS):
    pixels[i] = (0, 0, 0, 1)

pixels[0] = (255, 255, 0, 0)

r = random.randint(0, 63)
g = random.randint(0, 63)
b = random.randint(0, 63)
pixels[NUM_PIXELS - 1] = (r, g, b, 0)

for i in range(9):
    pixels.show()