#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

setup(
    name='touchpaper',
    version='0.1.0',
    description='A command-line utility to quickly launch EC2 instances. A tasty accompaniment to Fabric.',
    author='James Tiplady',
    url='http://github.com/BigglesZX/touchpaper',
    packages=find_packages(),
    install_requires=['boto==2.23.0'],
    entry_points={
        'console_scripts': [
            'touchpaper = touchpaper.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)