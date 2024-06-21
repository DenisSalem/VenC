#! /usr/bin/env python3

#   Copyright 2016, 2024 Denis Salem

#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_namespace_packages

print(find_namespace_packages(where="src"))

setup(
    name='VenC',
    version='3.3.0',
    description='A static blog generator.',
    author='Denis Salem',
    author_email='denissalem@tuxfamily.org',
    url='https://framagit.org/denissalem/VenC',
    license="GNU/GPLv3",
    platforms="Linux",
    long_description="A static and light blog generator, that aim to be damn fast and easy to use.",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
          'pyyaml',
          'unidecode'
    ],
    entry_points={
        'console_scripts': [
            'venc=venc3.main:venc_entry_point',
        ]
    },
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "venc3.package_data": ["*.json"],
        "venc3.package_data.themes.concrete": ["*.yaml"],
        "venc3.package_data.themes.concrete.assets": ["*.css"],
        "venc3.package_data.themes.concrete.chunks": ["*.html","*.xml"],
        "venc3.package_data.themes_assets": ["*.png","*.js"],
        "venc3.package_data.themes_templates": ["*"],
    },
    include_package_data=True
)
