#!/usr/bin/env python3

import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MITMsmtp",
    version="0.0.2",
    author="Robin Meis",
    author_email="blog@smartnoob.de",
    description="An evil SMTP Server for client pentesting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RobinMeis/MITMsmtp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'MITMsmtp = MITMsmtp.__main__:main'
        ]
    },
    include_package_data=True,
)
