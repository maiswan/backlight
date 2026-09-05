def rgbToHsl(red: float, green: float, blue: float):
    c_max = max(red, green, blue)
    c_min = min(red, green, blue)
    delta = c_max - c_min

    hue = 0
    if c_max == red:
        hue = 60 * ((green - blue) / delta % 6)
    elif c_max == green:
        hue = 60 * ((blue - red) / delta + 2)
    elif c_max == blue:
        hue = 60 * ((red - green) / delta + 4)

    lightness = (c_max + c_min) / 2

    saturation = 0
    if delta != 0:
        saturation = delta / (1 - abs(2 * lightness - 1))

    return (hue, saturation, lightness)


def HslToRgb(hue: float, saturation: float, lightness: float):
    c = (1 - abs(2 * lightness)) * saturation
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = lightness - c / 2

    if 0 <= hue < 60:
        return (c + m, x + m, m)
    elif 60 <= hue < 120:
        return (x + m, c + m, m)
    elif 120 <= hue < 180:
        return (m, c + m, x + m)
    elif 180 <= hue < 240:
        return (m, x + m, c + m)
    elif 240 <= hue < 300:
        return (x + m, 0, c + m)
    return (c + m, m, x + m)
