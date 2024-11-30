import os
from gifing import Gif


def test_get_images():
    gif = Gif(
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
    assert len(images) == 4
