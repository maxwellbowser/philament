from distutils.core import setup

from setuptools import find_packages

import os

# Optional project description in README.md:

current_directory = os.path.dirname(os.path.abspath(__file__))

try:

    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:

        long_description = f.read()

except Exception:

    long_description = "Sorry, an Exception was encountered"

setup(
    # Project name:
    name="philament-tracker",
    # Packages to include in the distribution:
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # Project version number:
    version="0.1.0",
    # List a license for the project, eg. MIT License
    license="BSD-3-Clause",
    # Short description of your library:
    description="Automated Tracking and Speed Analysis of Centroid Objects",
    # Long description of your library:
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Your name:
    author="Ryan M. Bowser",
    # Your email address:
    author_email="Ryanmaxwellbowser@gmail.com",
    # Link to your github repository or website:
    url="",
    # Download Link from where the project can be downloaded from:
    download_url="",
    # List of keywords:
    keywords=[
        "Tracking",
        "Automation",
        "Research",
        "Biology",
        "Actin",
        "Myosin",
        "In Vitro Motility",
    ],
    # List project dependencies:
    install_requires=["numpy", "pandas", "trackpy", "pims", "tifffile", "cv2"],
    # https://pypi.org/classifiers/
    classifiers=[],
)
