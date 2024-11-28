import pytest
from PIL import Image

from gifing.main import _set_size_and_background


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    img = Image.new("RGB", (200, 300), color="red")
    return img


def test_set_size_and_background_resize(sample_image):
    """Test that the image is resized and placed on background correctly."""
    target_size = (1000, 1000)
    background_color = (255, 255, 255)

    resized_image = _set_size_and_background(
        sample_image, target_size, background_color
    )

    assert resized_image.size == target_size

    corner_pixel = resized_image.getpixel((0, 0))
    assert corner_pixel == background_color

    center_x, center_y = target_size[0] // 2, target_size[1] // 2
    center_pixel = resized_image.getpixel((center_x, center_y))
    assert center_pixel == (255, 0, 0)  # original red color


def test_set_size_and_background_different_aspect_ratios():
    """Test resizing with different aspect ratios."""
    # Wide image
    wide_img = Image.new("RGB", (400, 100), color="blue")
    target_size = (1000, 1000)
    resized_wide = _set_size_and_background(wide_img, target_size, (255, 255, 255))
    assert resized_wide.size == target_size

    # Tall image
    tall_img = Image.new("RGB", (100, 400), color="green")
    resized_tall = _set_size_and_background(tall_img, target_size, (255, 255, 255))
    assert resized_tall.size == target_size
