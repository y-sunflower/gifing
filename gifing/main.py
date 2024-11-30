import numpy as np
import imageio
from PIL import Image, ImageFile, ImageDraw, ImageFont
from PIL.Image import Resampling
from typing import Union, Tuple, List, Dict, Optional
import importlib.resources as pkg_resources
import warnings

from .utils.colors import _strcolor_to_rgb


class Gif:
    def __init__(
        self,
        file_path: List[str],
        frame_duration: int = 1000,
        n_repeat_last_frame: int = 1,
    ):
        """
        Initialize the GIF maker.

        :param file_path: List of file paths to the images to be included in the GIF.
        :param frame_duration: Duration of each frame in milliseconds.
        :param n_repeat_last_frame: The number of additional frames to append with the last image.
        """
        self.file_path = file_path
        self.frame_duration = frame_duration
        self.n_repeat_last_frame = n_repeat_last_frame
        self.labels = {}
        self.size = (1000, 1000)
        self.scale = 1
        self.background_color = (255, 255, 255)

        ImageFile.LOAD_TRUNCATED_IMAGES = True

    def set_size(
        self,
        size: Tuple[int, int],
        scale: int = 1,
    ):
        """
        :param size: The size of the output GIF (width, height) in pixels.
        :param scale: Scaling factor to adjust the size of the images in the GIF.
        """
        self.size = size
        self.scale = scale

    def set_background_color(
        self,
        background_color: Union[str, Tuple[int, int, int]],
    ) -> None:
        """
        :param background_color: The RGB color or string name of the background for each frame.
        Default is (255, 255, 255) (white). Strings can be names of colors such as "white", "black",
        "red", "green", "blue", "yellow", "cyan", "magenta", "gray", "orange", "purple" or "pink".
        :returns: None
        """
        if isinstance(background_color, str):
            background_color = _strcolor_to_rgb(background_color)
        self.background_color = background_color

    def set_labels(
        self,
        labels: Dict[int, Dict[str, Union[str, int]]],
    ) -> None:
        """
        Set labels for specific frames in the GIF.

        :param labels: Dictionary where keys are frame indices (0-based) and values are dictionaries
                    containing 'text' (str) and 'size' (int) keys.
                    Example: {0: {'text': 'Frame 1', 'size': 24}, 1: {'text': 'Frame 2', 'size': 24}}
        """
        self.labels = labels

    def make(
        self,
        output_path: str = "./output.gif",
    ) -> None:
        """
        Creates and saves a GIF.

        :param output_path: Path where the output GIF will be saved. Default is "./output.gif".
        :returns: None
        """
        self.output_path = output_path

        images_for_gif = []

        self.dim = (self.size[0] * self.scale, self.size[1] * self.scale)

        if not self.output_path.endswith(".gif"):
            warnings.warn("The output path does not have a '.gif' extension.")
            self.output_path += ".gif"

        for idx, filename in enumerate(self.file_path):
            with Image.open(filename) as img:
                img = self._format_image(img, frame_idx=idx)
                img_array = np.array(img)
                images_for_gif.append(img_array)

        last_frame = images_for_gif[-1]
        for _ in range(self.n_repeat_last_frame):
            images_for_gif.append(last_frame)

        self.images_for_gif = images_for_gif

        imageio.mimsave(
            f"{output_path}",
            self.images_for_gif,
            duration=[self.frame_duration] * len(self.images_for_gif),
            format="GIF",
            loop=0,
        )
        print(f"GIF created and saved at {output_path}")

    def get_images(self) -> List:
        return self.images_for_gif

    def _format_image(self, image, frame_idx: Optional[int] = None):
        img_w, img_h = image.size
        bg_w, bg_h = self.size
        scale = min(bg_w / img_w, bg_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        image = image.resize((new_w, new_h), Resampling.LANCZOS)
        new_image = Image.new("RGB", self.size, self.background_color)
        new_image.paste(image, ((bg_w - new_w) // 2, (bg_h - new_h) // 2))

        if frame_idx is not None and frame_idx in self.labels:
            label_info = self.labels[frame_idx]
            draw = ImageDraw.Draw(new_image)
            with pkg_resources.path("gifing.fonts", "Urbanist-Bold.ttf") as font_path:
                font = ImageFont.truetype(font_path, label_info["size"])

            text_bbox = draw.textbbox(
                (0, 0), label_info["text"], font=font, font_size=label_info["size"]
            )
            text_width = text_bbox[2] - text_bbox[0]
            padding = 10
            x = bg_w - text_width - padding
            y = padding

            draw.text((x, y), label_info["text"], font=font, fill=(0, 0, 0))

        return new_image
