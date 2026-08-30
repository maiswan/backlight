# https://docs.circuitpython.org/projects/neopixel/en/latest/_modules/neopixel.html
from enum import StrEnum

class PixelOrder(StrEnum):
    RGB = "RGB"
    GRB = "GRB"
    BGR = "BGR"
    RGBW = "RGBW"
    GRBW = "GRBW"