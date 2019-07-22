# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('vim2vsc/convert.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "vim2vsc",
    packages = ["vim2vsc"],
    entry_points = {
        "console_scripts": ['vim2vsc = vim2vsc.convert:main']
        },
    version = version,
    description = "Python command line application to convert vimrc to vscode compatible bindings.",
    long_description = long_descr,
    author = "Devanshu Desai",
    author_email = "dbdesai@ucsd.edu",
    url = "http://gehrcke.de/2014/02/distributing-a-python-command-line-application",
    )
