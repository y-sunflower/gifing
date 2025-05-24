import numpy as np
import imageio
from PIL import Image, ImageFile
from PIL.Image import Resampling
from typing import Union, Tuple, List
import warnings

from .colors import _strcolor_to_rgb


class GIF:
    def __init__(
        self,
        file_path: List[str],
        frame_duration: int = 1000,
        n_repeat_last_frame: int = 1,
        verbose: bool = True,
    ):
        """
        Initialize the GIF maker.

        Parameters
        - file_path: List of file paths to the images to be included in the GIF.
        - frame_duration: Duration of each frame in milliseconds.
        - n_repeat_last_frame: The number of additional frames to append with the last image.
        - verbose: whether to print things in the console.
        """
        self.file_path = file_path
        self.frame_duration = frame_duration
        self.n_repeat_last_frame = n_repeat_last_frame
        self.size = (500, 500)
        self.scale = 1
        self.background_color = (255, 255, 255)
        self.images_for_gif = [None] * len(file_path)
        self.verbose = verbose
        ImageFile.LOAD_TRUNCATED_IMAGES = True

    def set_size(
        self,
        size: Tuple[int, int],
        scale: int = 1,
    ):
        """
        Set the size (width, height) and scale (default 1) of each image.

        Parameters
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
        Set the background color to use when images have different size.

        Parameters
        - background_color: The RGB color, hex color or string name of the
        background for each frame. Default is (255, 255, 255) (white). Strings
        can be names of colors such as "white", "black", "red", "green",
        "blue", "yellow", "cyan", "magenta", "gray", "orange", "purple" or "pink".
        """
        if isinstance(background_color, str):
            background_color = _strcolor_to_rgb(background_color)
        self.background_color = background_color

    def make(
        self,
        output_path: str = "output.gif",
    ) -> None:
        """
        Make (and save) a GIF.

        - output_path: path where the output GIF will be saved.
        """
        self.output_path = output_path

        images_for_gif = []

        self.dim = (round(self.size[0] * self.scale), round(self.size[1] * self.scale))

        if not self.output_path.endswith(".gif"):
            warnings.warn("The output path does not have a '.gif' extension.")
            self.output_path += ".gif"

        for i, filename in enumerate(self.file_path):
            print(f"\u2714 Gifing: {filename}")
            with Image.open(filename) as img:
                img = self._format_image(img)
                img_array = np.array(img)
                images_for_gif.append(img_array)

        last_frame = images_for_gif[-1]
        for _ in range(self.n_repeat_last_frame - 1):
            images_for_gif.append(last_frame)

        self.images_for_gif = images_for_gif

        imageio.mimsave(
            f"{self.output_path}",
            self.images_for_gif,
            duration=[self.frame_duration] * len(self.images_for_gif),
            format="GIF",
            loop=0,
        )

        if self.verbose:
            print(f"GIF created and saved at {output_path}")

    def get_images(self) -> List:
        """
        Retrieve a list with all the images
        """
        if not np.any(self.images_for_gif):
            raise Exception("Unable to retrieve images before calling GIF.make()")
        else:
            return self.images_for_gif

    def _format_image(self, image):
        img_w, img_h = image.size
        bg_w, bg_h = self.dim
        self.bg_w = bg_w
        self.bg_h = bg_h
        scale = min(bg_w / img_w, bg_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        image = image.resize((new_w, new_h), Resampling.LANCZOS)
        new_image = Image.new("RGB", self.dim, self.background_color)
        new_image.paste(image, ((bg_w - new_w) // 2, (bg_h - new_h) // 2))
        return new_image
