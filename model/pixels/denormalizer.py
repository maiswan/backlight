from ..renderer import RgbTuple

class Denormalizer:
    @staticmethod
    def toRgbwTuple(tuple: RgbTuple):
        red = int(min(max(0, tuple[0] * 255), 255))
        green = int(min(max(0, tuple[1] * 255), 255))
        blue = int(min(max(0, tuple[2] * 255), 255))

        # Offload as much brightness to white LED as possible
        white = min(red, green, blue)
        red -= white
        green -= white
        blue -= white
        return (red, green, blue, white)

    @staticmethod
    def toRgbTuple(tuple: RgbTuple):
        red = int(min(max(0, tuple[0] * 255), 255))
        green = int(min(max(0, tuple[1] * 255), 255))
        blue = int(min(max(0, tuple[2] * 255), 255))
        return (red, green, blue)