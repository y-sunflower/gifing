import pytest
from unittest.mock import patch
from gifing import Gif


# @patch("gifing.imageio.mimsave")  # Patching the correct module path
# def test_make(mock_mimsave):
#     gif = Gif(file_path=["image1.jpg", "image2.jpg"])
#     gif.set_size((500, 500), scale=2)
#     gif.set_background_color("blue")

#     mock_mimsave.return_value = None  # Mock mimsave to prevent actual file writing
#     gif.make(output_path="test_output.gif")

#     mock_mimsave.assert_called_once_with(
#         "test_output.gif",
#         gif.get_images(),
#         duration=[gif.frame_duration] * len(gif.get_images()),
#         format="GIF",
#         loop=0,
#     )
