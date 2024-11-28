import numpy as np
import imageio
from PIL import Image, ImageFile
from PIL.Image import Resampling
from typing import Union, Tuple, List

from .utils import _strcolor_to_rgb

ImageFile.LOAD_TRUNCATED_IMAGES = True


def _set_size_and_background(
    image, size: tuple, background_color: Union[str, Tuple[int, int, int]]
):
    """
    Resizes an image while maintaining its aspect ratio and places it on a background of the specified size and color.

    Args:
        image (PIL.Image.Image): The image to be resized and placed on a background.
        size (tuple): The size of the background (width, height) in pixels.
        background_color (tuple): The RGB color of the background.

    Returns:
        PIL.Image.Image: The resized image centered on the background.
    """
    img_w, img_h = image.size
    bg_w, bg_h = size
    scale = min(bg_w / img_w, bg_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    image = image.resize((new_w, new_h), Resampling.LANCZOS)
    new_image = Image.new("RGB", size, background_color)
    new_image.paste(image, ((bg_w - new_w) // 2, (bg_h - new_h) // 2))
    return new_image


def gif(
    file_path: List[str],
    frame_duration: int = 1000,
    size: Tuple[int, int] = (1000, 1000),
    background_color: Union[str, Tuple[int, int, int]] = (255, 255, 255),
    output_path: str = "./output.gif",
    n_repeat_last_frame: int = 1,
    size_scale: int = 1,
) -> None:
    """
    Creates a GIF from a sequence of image files.

    Args:
        - file_path (List[str]): List of file paths to the images to be included in the GIF.
        - frame_duration (int, optional): Duration of each frame in milliseconds. Default is 1000ms.
        - size (Tuple[int, int], optional): The size of the output GIF (width, height) in pixels. Default is (1000, 1000).
        - background_color (Union[str, Tuple[int, int, int]], optional): The RGB color or string name of the background
        for each frame. Default is (255, 255, 255) (white). Strings can be names of colors such as "white", "black", "red",
        "green", "blue", "yellow", "cyan", "magenta", "gray", "orange", "purple" or "pink".
        - output_path (str, optional): Path where the output GIF will be saved. Default is "./output.gif".
        - n_repeat_last_frame (int, optional): The number of additional frames to append with the last image. Default is 1.
        - size_scale (int, optional): Scaling factor to adjust the size of the images in the GIF. Default is 1 (no scaling).

    Returns:
        None
    """
    images_for_gif = []

    size = (size[0] * size_scale, size[1] * size_scale)

    if isinstance(background_color, str):
        background_color = _strcolor_to_rgb(background_color)

    if not output_path.endswith(".gif"):
        output_path += ".gif"

    for filename in file_path:
        with Image.open(filename) as img:
            img = _set_size_and_background(img, size, background_color)
            img_array = np.array(img)
            images_for_gif.append(img_array)

    last_frame = images_for_gif[-1]
    for _ in range(n_repeat_last_frame):
        print("here")
        images_for_gif.append(last_frame)

    imageio.mimsave(
        f"{output_path}",
        images_for_gif,
        duration=[frame_duration] * len(images_for_gif),
        format="GIF",
        loop=0,
    )
    print(f"GIF created and saved at {output_path}")
