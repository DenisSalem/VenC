#! /usr/bin/env python3

#   Copyright 2016, 2019 Denis Salem

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

from os.path import expanduser, isdir
from os import listdir
from setuptools import setup


dst_themes_path = expanduser('~')+"/.local/share/VenC/themes/"
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
            print(dst, src_files)
            
        extra_files.append((
            dst,
            src_files
        ))
            
        
extra_files.append((expanduser('~')+"/.local/share/VenC/embed_providers/",  ["share/embed_providers/oembed.json"]))
extra_files.append((expanduser('~')+"/.local/share/VenC/themes_assets",    ["share/themes_assets/"+filename for filename in listdir("share/themes_assets")]) )

setup(
    name='VenC',
    version='2.0.0',
    description='A static blog generator.',
    author='Denis Salem',
    author_email='denissalem@tuxfamily.org',
    url='https://github.com/DenisSalem/VenC',
    packages=[
        'venc2',
        'venc2.commands',
        'venc2.datastore',
        'venc2.l10n',
        'venc2.patterns',
        'venc2.threads'
    ],
    license="GNU/GPLv3",
    platforms="Linux",
    long_description="A static and light blog generator, Aim to be easy to use.",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable"
    ],
    install_requires=[
          "docutils",
          "latex2mathml",
          'markdown2',
          'pyyaml',
          'Pygments',
          "requests"
    ],
    scripts=['venc','venc-blog-migration'],
    data_files = extra_files
)
