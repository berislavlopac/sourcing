#!/usr/bin/env python3
from setuptools import setup, find_packages

with open('README.md') as readme:
    long_desc = readme.read()

setup(
    name="nods",
    version="0.0.1",
    description="A lightweight library for event sourcing in Python.",
    long_description=long_desc,
    author="Sky Core Tools Team",
    url="https://git.bskyb.com/gcp/nods",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
        "sqlalchemy~=1.2",
        "tinydb~=3.11",
        "lmdb~=0.94",
        "msgpack~=0.5",
        "kafka-python~=1.4",
    ]
)
