#! /usr/bin/env python3

#   Copyright 2016, 2021 Denis Salem

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

from os.path import isdir
from os import listdir
from setuptools import setup

import site
import sys

# Workaround to have both installation procedure from setup.py and pip
# copying data files in the right place. 

dst_prefix = site.USER_BASE+'/' if ' '.join(sys.argv) == "./setup.py install --user" else ''

dst_themes_path = dst_prefix+"share/VenC/themes/"
src_themes_path = "share/themes/"
themes = listdir(src_themes_path)

extra_files = []
for theme in themes:
    for filename in listdir(src_themes_path+theme+'/'):
        if isdir(src_themes_path+theme+'/'+filename):
            dst = dst_themes_path+theme+'/'+filename
            src_files = [src_themes_path+theme+'/'+filename+'/'+f for f in listdir(src_themes_path+theme+'/'+filename)]

        else:
            dst = dst_themes_path+theme
            src_files = [src_themes_path+theme+'/'+filename]
            
        extra_files.append((
            dst,
            src_files
        ))
            
extra_files.append(
    (
        dst_prefix+"share/VenC/embed_providers/", 
        ["share/embed_providers/oembed.json"]
    )
)

extra_files.append(
    (
        dst_prefix+"share/VenC/themes_assets/",
        ["share/themes_assets/"+filename for filename in listdir("share/themes_assets") if not isdir("share/themes_assets/"+filename) ]
    )

)

extra_files.append(
    (
        dst_prefix+"share/VenC/themes_templates/",
        ["share/themes_templates/"+filename for filename in listdir("share/themes_templates")]
    )
)

setup(
    name='VenC',
    version='3.1.0',
    description='A static blog generator.',
    author='Denis Salem',
    author_email='denissalem@tuxfamily.org',
    url='https://github.com/DenisSalem/VenC',
    packages=[
        'venc3',
        'venc3.commands',
        'venc3.datastore',
        'venc3.l10n',
        'venc3.markup_languages',
        'venc3.parallelism',
        'venc3.patterns',
        'venc3.patterns.third_party_wrapped_features',
        'venc3.threads'
    ],
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
    scripts=['venc'],
    data_files = extra_files
)
