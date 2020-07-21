import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Tropical2020",
    version="0.0.1",
    author="Mathieu Foucher <mathieu.foucher@colorado.edu>, " +
           "Connor Meredith <connor.meredith@colorado.edu>, " +
           "Jonathan Wise <jonathan.wise@colorado.edu>",
    description="A package implementing concepts from Tropical Geometry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mat-foucher/Tropical2020",
    packages=setuptools.find_packages(),
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
