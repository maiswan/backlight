def hsv2rgb(h, s, v):
    """
    Convert HSV color space to RGB.
    h: Hue, in [0, 360)
    s: Saturation, in [0, 1]
    v: Value, in [0, 1]
    Returns (r, g, b) with values in [0, 255]
    """
    if s == 0.0:
        r = g = b = int(v * 255)
        return r, g, b

    h = h % 360
    h_sector = h / 60
    i = int(h_sector)
    f = h_sector - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))

    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return int(r * 255), int(g * 255), int(b * 255)