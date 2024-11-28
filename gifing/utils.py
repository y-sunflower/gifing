def _strcolor_to_rgb(color: str):
    """
    Converts a basic color name to its RGB tuple.

    Args:
        color (str): The name of the color (case insensitive).

    Returns:
        tuple: An (R, G, B) tuple representing the color, or None if the color is not found.
    """
    color_map = {
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

    color = color.lower()
    if color not in color_map:
        raise ValueError(
            f"Invalid color name: '{color}'. Valid colors are: {', '.join(color_map.keys())}."
        )

    return color_map[color]
