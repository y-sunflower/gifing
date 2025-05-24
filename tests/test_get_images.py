import os
import pytest
from gifing import GIF


def test_get_images_before_make():
    gif = GIF(
        file_path=[
            "tests/img/image1.jpg",
            "tests/img/image2.jpg",
            "tests/img/image3.jpg",
        ]
    )
    gif.set_size((500, 500), scale=2)
    gif.set_background_color("yellow")

    with pytest.raises(Exception):
        gif.get_images()


def test_get_images_after_make():
    gif = GIF(
        file_path=[
            "tests/img/image1.jpg",
            "tests/img/image2.jpg",
            "tests/img/image3.jpg",
        ]
    )
    gif.set_size((500, 500), scale=2)
    gif.set_background_color("yellow")
    gif.make("test_output.gif")
    os.remove(gif.output_path)

    images = gif.get_images()
    assert len(images) == 3
    assert len(images) == len(gif.file_path)
