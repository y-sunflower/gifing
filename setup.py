from setuptools import setup, find_packages

setup(
    name="gifing",
    version="0.1.0",
    packages=find_packages(),
    description="A super lightweight python tool for creating GIFs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Joseph Barbier",
    author_email="joseph.barbierdarnal@gmail.com",
    url="https://github.com/JosephBARBIERDARNAL/gifing/blob/main/README.md",
    install_requires=["imageio", "numpy"],
)
