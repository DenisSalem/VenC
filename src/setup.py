#!/usr/bin/python3

from distutils.core import setup

setup(name='VenC',
    version='1.2.0',
    description='A static blog generator',
    author='Denis Salem',
    author_email='denissalem@tuxfamily.org',
    url='https://github.com/DenisSalem/VenC',
    packages=['VenC', 'VenC.languages'],
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable"
    ]
)