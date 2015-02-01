__author__ = 'adrian'
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "google_drive_backup",
    version = "0.0.1",
    author = "Adrian Spataru",
    author_email = "florin.spataru92@e-uvt.ro",
    description = ("An demonstration of google drive api."),
    license = "Apache 2.0 License",
    keywords = "google drive backup",
    url = "",
    packages=['gds', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires = [
        'google-api-python-client>=1.1',
    ],

    entry_points={
        'console_scripts': [
            'gsd = gds.GDS:main',
        ],
    },
)
