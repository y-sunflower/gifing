# gifing

A lightweight python tool for creating GIF

<br>

## Quick start

Let's make a GIF with these images:

<p align="center">
  <img src="https://github.com/y-sunflower/gifing/blob/main/tests/img/image2.jpg?raw=true" width="25%" />
  <img src="https://github.com/y-sunflower/gifing/blob/main/tests/img/image1.jpg?raw=true" width="25%" />
  <img src="https://github.com/y-sunflower/gifing/blob/main/tests/img/image3.jpg?raw=true" width="25%" />
</p>

```python
from gifing import GIF

path = "tests/img/image"
path_to_files = [f"{path}1.jpg", f"{path}2.jpg", f"{path}3.jpg",]

gif = GIF(
  path_to_files,
  frame_duration=500,      # in ms
  n_repeat_last_frame=3,   # 500x3
)
gif.set_background_color("red")
gif.set_size((900, 700), scale=1.2)
gif.make("img/output.gif")
```

![](https://github.com/y-sunflower/gifing/blob/main/img/output.gif?raw=true)

This package offers:

- a streamlined approach to creating GIF
- automatic image resizing
- ability to set a background color during resizing

> It's a basic prototype of the functionality I envision for this tool. The API is still **unstable**.

<br>

## Installation

Install directly via pip (requires Python >=3.9):

```bash
pip install gifing
```

<br><br>

## Usage

Import the `GIF` class and provide a list of image file paths:

```python
from gifing import GIF

path = "tests/img"
gif = GIF(
    [f"{path}/image{i}.jpg" for i in range(1, 4)],
    frame_duration=800,  # Duration per frame (in milliseconds)
    n_repeat_last_frame=3,  # Repeat last frame 3x longer
)
```

You can set a background color, which is useful if your images have varying sizes:

```python
gif.set_background_color("black")
```

You can also set a custom size for your GIF. The `set_size` method allows you to specify a target size and scale factor:

```python
gif.set_size((300, 800), scale=2) # (600px, 1600px)
```

Finally, call the `make()` method to generate the GIF:

```python
gif.make("path/to/output/file.gif")
```

If not specified, by default, the GIF will be saved as `output.gif`.
