from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(
    name='touchpaper',
    version=version,
    package_dir={'': 'src'},
    packages=find_packages('src'),
)

