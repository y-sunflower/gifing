import os
import imageio
from PIL import Image
import pytest

from gifing import gif


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    img = Image.new("RGB", (200, 300), color="red")
    return img


def test_gif_creation(tmp_path):
    """Test GIF creation with sample images."""
    d = tmp_path / "subdir"
    d.mkdir()
    image1_path = d / "image1.png"
    image2_path = d / "image2.png"

    Image.new("RGB", (200, 300), color="red").save(image1_path)
    Image.new("RGB", (200, 300), color="blue").save(image2_path)

    output_path = d / "output.gif"

    gif(
        file_path=[str(image1_path), str(image2_path)],
        frame_duration=500,
        size=(1000, 1000),
        background_color="white",
        output_path=str(output_path),
        n_repeat_last_frame=2,
    )

    assert os.path.exists(output_path)

    gif_frames = imageio.mimread(str(output_path))

    for frame in gif_frames:
        assert frame.shape == (1000, 1000, 3)


def test_gif_output_filename():
    """Test that .gif is appended to output path if not present."""
    img = Image.new("RGB", (200, 300), color="red")
    img_path = "./temp_image.png"
    img.save(img_path)

    output_path1 = "./output"
    output_path2 = "./output.gif"

    try:
        gif(file_path=[img_path], output_path=output_path1)
        assert os.path.exists(output_path1 + ".gif")

        gif(file_path=[img_path], output_path=output_path2)
        assert os.path.exists(output_path2)
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)
        if os.path.exists(output_path1 + ".gif"):
            os.remove(output_path1 + ".gif")
        if os.path.exists(output_path2):
            os.remove(output_path2)


def test_gif_size_scaling():
    """Test GIF creation with size scaling."""
    img = Image.new("RGB", (200, 300), color="red")
    img_path = "./temp_image.png"
    img.save(img_path)

    output_path = "./scaled_output.gif"

    try:
        gif(
            file_path=[img_path],
            size=(500, 500),
            size_scale=2,
            output_path=output_path,
            n_repeat_last_frame=2,
        )

        assert os.path.exists(output_path)

        gif_frames = imageio.mimread(output_path)

        for frame in gif_frames:
            assert frame.shape == (1000, 1000, 3)
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)
        if os.path.exists(output_path):
            os.remove(output_path)


def test_invalid_input():
    """Test handling of invalid inputs."""
    with pytest.raises(Exception):
        gif(file_path=[])

    with pytest.raises(FileNotFoundError):
        gif(file_path=["non_existent_file.png"])
