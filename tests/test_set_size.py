from gifing import GIF


def test_set_size():
    gif = GIF(file_path=["image1.jpg", "image2.jpg"])
    gif.set_size((500, 500), scale=2)
    assert gif.size == (500, 500)
    assert gif.scale == 2
