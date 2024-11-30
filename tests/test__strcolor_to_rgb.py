import pytest
from gifing import Gif


def test__strcolor_to_rgb():
    gif = Gif([])
    assert gif._strcolor_to_rgb("red") == (255, 0, 0)
    assert gif._strcolor_to_rgb("blue") == (0, 0, 255)
    assert gif._strcolor_to_rgb("green") == (0, 255, 0)

    with pytest.raises(ValueError):
        gif._strcolor_to_rgb("invalid_color")
