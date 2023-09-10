from setuptools import setup, find_packages, Extension
from distutils.core import setup, Extension
import sys
import os
import base64
import json

# read the contents of the README
with open('README.md') as README_md:
    README = README_md.read()



if sys.platform == 'darwin':
    pass