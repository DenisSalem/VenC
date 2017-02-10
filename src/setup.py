#!/usr/bin/python3

from setuptools import setup

setup(name='VenC',
    version='1.2.0-2',
    description='A static blog generator.',
    author='Denis Salem',
    author_email='denissalem@tuxfamily.org',
    url='https://github.com/DenisSalem/VenC',
    packages=['VenC', 'VenC.languages'],
    license="GNU/GPLv3",
    platforms="Linux",
    long_description="A static blog generator, light and easy to use.",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable"
    ],
    install_requires=[
          'markdown',
          'pyyaml',
          'Pygments'
    ],
    scripts=['venc','venc-unit-test']
)
