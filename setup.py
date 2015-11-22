from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


setup(
    name="ConfigMaster",
    version='2.3.6',
    description="Programmatic configuration library for Python 3.",
    author="Isaac Dickinson",
    author_email="eyesismine@gmail.com",
    url="https://github.com/SunDwarf/ConfigMaster",
    packages=["configmaster"],
    license="MIT",
    tests_require=["tox", "tox-pyenv"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only"
    ],
)
