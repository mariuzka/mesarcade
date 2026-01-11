import matplotlib.colors


def parse_color(color) -> tuple[int, int, int, int]:
    r, g, b, a = matplotlib.colors.to_rgba(color)
    return (int(r * 255), int(g * 255), int(b * 255), int(a * 255))
