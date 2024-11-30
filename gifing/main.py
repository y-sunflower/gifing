import numpy as np
import imageio
from PIL import Image, ImageFile, ImageDraw, ImageFont
from PIL.Image import Resampling
from typing import Union, Tuple, List, Optional
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

        Parameters
        - file_path: List of file paths to the images to be included in the GIF.
        - frame_duration: Duration of each frame in milliseconds.
        - n_repeat_last_frame: The number of additional frames to append with the last image.
        """
        self.file_path = file_path
        self.frame_duration = frame_duration
        self.n_repeat_last_frame = n_repeat_last_frame
        self.labels = None
        self.size = (500, 500)
        self.scale = 1
        self.background_color = (255, 255, 255)
        self.label_loc = "top left"  # Default location
        ImageFile.LOAD_TRUNCATED_IMAGES = True

    def set_size(
        self,
        size: Tuple[int, int],
        scale: int = 1,
    ):
        """
        - size: The size of the output GIF (width, height) in pixels.
        - scale: Scaling factor to adjust the size of the images in the GIF.
        """
        self.size = size
        self.scale = scale

    def set_background_color(
        self,
        background_color: Union[str, Tuple[int, int, int]],
    ) -> None:
        """
        - background_color: The RGB color or string name of the background for each frame.
        Default is (255, 255, 255) (white). Strings can be names of colors such as "white", "black",
        "red", "green", "blue", "yellow", "cyan", "magenta", "gray", "orange", "purple" or "pink".
        :returns: None
        """
        if isinstance(background_color, str):
            background_color = _strcolor_to_rgb(background_color)
        self.background_color = background_color

    def set_labels(
        self,
        labels: List[str],
        font_size: int = 20,
        padding: int = 10,
        loc: str = "top left",  # Add location argument with default value
    ) -> None:
        """
        Set labels for specific frames in the GIF.
        """
        if loc not in ["top left", "top right", "bottom left", "bottom right"]:
            raise ValueError(
                "Invalid loc. Choose from 'top left', 'top right', 'bottom left', 'bottom right'."
            )
        self.labels = labels
        self.padding = padding
        self.font_size = font_size
        self.label_loc = loc  # Store the location

    def make(
        self,
        output_path: str = "./output.gif",
    ) -> None:
        """
        Creates and saves a GIF.

        - output_path: Path where the output GIF will be saved. Default is "./output.gif".
        :returns: None
        """
        self.output_path = output_path

        images_for_gif = []

        self.dim = (self.size[0] * self.scale, self.size[1] * self.scale)

        if not self.output_path.endswith(".gif"):
            warnings.warn("The output path does not have a '.gif' extension.")
            self.output_path += ".gif"

        for i, filename in enumerate(self.file_path):
            with Image.open(filename) as img:
                img = self._format_image(img, frame_idx=i)
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

        if self.labels is not None:
            label_text = self.labels[frame_idx]
            draw = ImageDraw.Draw(new_image)
            with pkg_resources.path("gifing.fonts", "Urbanist-Bold.ttf") as font_path:
                font = ImageFont.truetype(font_path, self.font_size)

            text_bbox = draw.textbbox(
                (0, 0), label_text, font=font, font_size=self.font_size
            )
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate position based on loc
            if self.label_loc == "top left":
                x = self.padding
                y = self.padding
            elif self.label_loc == "top right":
                x = bg_w - text_width - self.padding
                y = self.padding
            elif self.label_loc == "bottom left":
                x = self.padding
                y = bg_h - text_height - self.padding
            elif self.label_loc == "bottom right":
                x = bg_w - text_width - self.padding
                y = bg_h - text_height - self.padding

            draw.text((x, y), label_text, font=font, fill=(0, 0, 0))

        return new_image
