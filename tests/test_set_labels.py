import pytest
from gifing import Gif


def test_wrong_loc_labels_raises_warning():
    gif = Gif(
        file_path=[
            "tests/img/image1.jpg",
            "tests/img/image2.jpg",
            "tests/img/image3.jpg",
        ]
    )

    with pytest.raises(ValueError):
        gif.set_labels(["print", "hello", "world"], loc="invalid value")
