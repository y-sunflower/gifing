import pytest
from gifing.colors import (
    _is_hex_color,
    _is_named_color,
    _hex_to_rgb,
    _strcolor_to_rgb,
    COLOR_MAP,
)


class TestHexColorValidation:
    @pytest.mark.parametrize(
        "valid_hex",
        [
            "#FFF",
            "#fff",
            "#FFFFFF",
            "#ffffff",
            "#A1B2C3",
            "#a1b2c3",
        ],
    )
    def test_valid_hex_colors(self, valid_hex):
        assert _is_hex_color(valid_hex) is True

    @pytest.mark.parametrize(
        "invalid_hex",
        [
            "FFF",
            "#FFFFFFFF",
            "#GGG",
            "#12345",
            "##FFF",
            "#fff ",
            " #fff",
            "fff",
            "",
            "#",
            "#G",
            "#1Z",
        ],
    )
    def test_invalid_hex_colors(self, invalid_hex):
        assert _is_hex_color(invalid_hex) is False


class TestNamedColorValidation:
    @pytest.mark.parametrize("color_name", COLOR_MAP.keys())
    def test_valid_named_colors(self, color_name):
        assert _is_named_color(color_name) is True

    def test_invalid_named_colors(self):
        invalid_colors = [
            "red1",
            "dark red",
            "lightblue",
            "",
            "color",
            "123",
        ]
        for color in invalid_colors:
            assert _is_named_color(color) is False


class TestHexToRgbConversion:
    @pytest.mark.parametrize(
        "hex_color,expected_rgb",
        [
            ("#FFF", (255, 255, 255)),
            ("#fff", (255, 255, 255)),
            ("#000", (0, 0, 0)),
            ("#FF0000", (255, 0, 0)),
            ("#00FF00", (0, 255, 0)),
            ("#0000FF", (0, 0, 255)),
            ("#A1B2C3", (161, 178, 195)),
        ],
    )
    def test_hex_to_rgb_conversion(self, hex_color, expected_rgb):
        assert _hex_to_rgb(hex_color) == expected_rgb


class TestStrColorToRgbConversion:
    @pytest.mark.parametrize(
        "color_input,expected_rgb",
        [
            *[(color, rgb) for color, rgb in COLOR_MAP.items()],
            ("#FFF", (255, 255, 255)),
            ("#000", (0, 0, 0)),
            ("#FF0000", (255, 0, 0)),
        ],
    )
    def test_valid_color_conversions(self, color_input, expected_rgb):
        assert _strcolor_to_rgb(color_input) == expected_rgb

    def test_invalid_color_conversion_raises_value_error(self):
        invalid_colors = [
            "not_a_color",
            "red1",
            "#GGGGGG",
            "",
            "  ",
        ]
        for invalid_color in invalid_colors:
            with pytest.raises(
                ValueError, match=f"Invalid color name: '{invalid_color}'"
            ):
                _strcolor_to_rgb(invalid_color)
