#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

with open("README.rst", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pipeflow-lite",
    version="0.1.0",
    author="Leon",
    author_email="leon.hooo@outlook.com",
    description='A flexible and powerful data processing pipeline library',
    long_description=long_description,
    url='https://github.com/leonhoo/pipeflow-lite',
    install_requires=[],
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries'
    ]
)
