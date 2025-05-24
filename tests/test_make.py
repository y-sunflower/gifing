import pytest
import os
from gifing import GIF


def test_make_with_wrong_path_raises_warning():
    gif = GIF(
        file_path=[
            "tests/img/image1.jpg",
            "tests/img/image2.jpg",
            "tests/img/image3.jpg",
        ]
    )

    with pytest.warns():
        gif.make("output")
        os.remove(gif.output_path)


def test_resizing_and_scaling():
    gif = GIF(
        file_path=[
            "tests/img/image1.jpg",
            "tests/img/image2.jpg",
            "tests/img/image3.jpg",
        ]
    )
    gif.set_size((500, 600), scale=2)
    gif.make()
    os.remove(gif.output_path)

    images = gif.get_images()
    for i in range(len(gif.file_path)):
        assert len(images[i]) == 1200
