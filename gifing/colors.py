import re
from typing import Tuple, Dict

COLOR_MAP: Dict[str, Tuple[int]] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
}

NAMED_COLORS = set(COLOR_MAP.keys())


def _is_hex_color(color_string):
    # starts with #, followed by 3 or 6 hexadecimal characters
    hex_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(hex_pattern, color_string))


def _is_named_color(color_string):
    return color_string.lower() in NAMED_COLORS


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        return tuple(int(c * 2, 16) for c in hex_color)
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def _strcolor_to_rgb(color: str):
    if _is_hex_color(color):
        return _hex_to_rgb(color)
    elif _is_named_color(color):
        return COLOR_MAP[color]
    else:
        raise ValueError(
            f"Invalid color name: '{color}'."
            " `color` must be a hex color or one of the following:\n"
            f"{', '.join(COLOR_MAP.keys())}."
        )
