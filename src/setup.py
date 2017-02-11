#!/usr/bin/python3

from setuptools import setup
import os

setup(name='VenC',
    version='1.2.0-3',
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
    scripts=['venc','venc-unit-test'],
    data_files=[
        
        ### DUMMY

        (
            os.path.expanduser("~")+'/.local/share/VenC/themes/dummy/chunks',
            [
                'share/themes/dummy/chunks/header.html',
                'share/themes/dummy/chunks/entry.html',
                'share/themes/dummy/chunks/footer.html',
                'share/themes/dummy/chunks/rssHeader.html',
                'share/themes/dummy/chunks/rssEntry.html',
                'share/themes/dummy/chunks/rssFooter.html'
            ]
        ),
        (
            os.path.expanduser("~")+'/.local/share/VenC/themes/dummy/assets',
            [
                'share/themes/dummy/assets/VenC-Infinite-Scroll-1.0.0.js'
            ]
        ),
        
        ### TESSELLATION

        (
            os.path.expanduser("~")+'/.local/share/VenC/themes/tessellation/chunks',
            [
                'share/themes/tessellation/chunks/header.html',
                'share/themes/tessellation/chunks/entry.html',
                'share/themes/tessellation/chunks/footer.html',
                'share/themes/tessellation/chunks/rssHeader.html',
                'share/themes/tessellation/chunks/rssEntry.html',
                'share/themes/tessellation/chunks/rssFooter.html'
            ]
        ),
        (
            os.path.expanduser("~")+'/.local/share/VenC/themes/tessellation/assets',
            [
                'share/themes/tessellation/assets/VenC-Infinite-Scroll-1.0.0.js',
                'share/themes/tessellation/assets/style.css',
                'share/themes/tessellation/assets/styleEntry.css',
                'share/themes/tessellation/assets/styleThread.css'
            ]
        ),
        
        ### GENTLE

        (
            os.path.expanduser("~")+'/.local/share/VenC/themes/gentle/chunks',
            [
                'share/themes/gentle/chunks/header.html',
                'share/themes/gentle/chunks/entry.html',
                'share/themes/gentle/chunks/footer.html',
                'share/themes/gentle/chunks/rssHeader.html',
                'share/themes/gentle/chunks/rssEntry.html',
                'share/themes/gentle/chunks/rssFooter.html'
            ]
        ),
        (
            os.path.expanduser("~")+'/.local/share/VenC/themes/gentle/assets',
            [
                'share/themes/gentle/assets/VenC-Infinite-Scroll-1.0.0.js',
                'share/themes/gentle/assets/style.css'
            ]
        )
    ]
)
