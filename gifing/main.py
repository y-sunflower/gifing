import numpy as np
import imageio
from PIL import Image, ImageFile
from PIL.Image import Resampling

ImageFile.LOAD_TRUNCATED_IMAGES = True


def add_background(image, size, background_color):
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
    file_path: list,
    frame_duration: int = 1000,
    size: tuple = (1000 * 3, 700 * 3),
    background_color=(255, 255, 255),
    output_path: str = "./output.gif",
    time_on_last_frame: int = 1,
):
    images_for_gif = []

    for filename in file_path:
        with Image.open(filename) as img:
            img_with_bg = add_background(img, size, background_color)
            img_array = np.array(img_with_bg)
            images_for_gif.append(img_array)

    last_frame = images_for_gif[-1]
    for _ in range(time_on_last_frame):
        images_for_gif.append(last_frame)

    imageio.mimsave(
        f"{output_path}",
        images_for_gif,
        duration=[frame_duration] * len(images_for_gif),
        format="GIF",
        loop=0,
    )
    print(f"GIF created and saved at {output_path}")
