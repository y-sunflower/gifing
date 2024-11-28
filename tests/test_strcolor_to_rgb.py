import pytest

from gifing.utils import _strcolor_to_rgb


def test_strcolor_to_rgb_valid_colors():
    assert _strcolor_to_rgb("white") == (255, 255, 255)
    assert _strcolor_to_rgb("black") == (0, 0, 0)
    assert _strcolor_to_rgb("red") == (255, 0, 0)
    assert _strcolor_to_rgb("green") == (0, 255, 0)
    assert _strcolor_to_rgb("blue") == (0, 0, 255)
    assert _strcolor_to_rgb("yellow") == (255, 255, 0)
    assert _strcolor_to_rgb("cyan") == (0, 255, 255)
    assert _strcolor_to_rgb("magenta") == (255, 0, 255)
    assert _strcolor_to_rgb("gray") == (128, 128, 128)
    assert _strcolor_to_rgb("orange") == (255, 165, 0)
    assert _strcolor_to_rgb("purple") == (128, 0, 128)
    assert _strcolor_to_rgb("pink") == (255, 192, 203)
    assert _strcolor_to_rgb("brown") == (165, 42, 42)


def test_strcolor_to_rgb_case_insensitivity():
    assert _strcolor_to_rgb("White") == (255, 255, 255)
    assert _strcolor_to_rgb("BlAcK") == (0, 0, 0)
    assert _strcolor_to_rgb("ReD") == (255, 0, 0)


def test_strcolor_to_rgb_invalid_color():
    with pytest.raises(ValueError, match="Invalid color name: 'unknown'"):
        _strcolor_to_rgb("unknown")
    with pytest.raises(ValueError, match="Invalid color name: '123'"):
        _strcolor_to_rgb("123")
    with pytest.raises(ValueError, match="Invalid color name: ''"):
        _strcolor_to_rgb("")
