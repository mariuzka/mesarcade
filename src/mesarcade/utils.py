import matplotlib.colors


def parse_color(color) -> tuple[int, int, int, int]:
    # RGB(A) tuples with values in 0-255
    if isinstance(color, (tuple, list)) and any(c > 1 for c in color):
        r, g, b, *a = color
        return (int(r), int(g), int(b), int(a[0]) if a else 255)

    r, g, b, a = matplotlib.colors.to_rgba(color)
    return (int(r * 255), int(g * 255), int(b * 255), int(a * 255))
