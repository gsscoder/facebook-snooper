# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from facebook_snooper.__version__ import __version__

# Package meta-data
NAME = 'facebook-snooper'
DESCRIPTION = 'Scrapes Facebook profile pages and searches profiles using a normal log in (without an API key).'
URL = 'https://github.com/bisguzar/twitter-scraper'
EMAIL = 'gsscoder@gmail.com'
AUTHOR = 'Giacomo Stelluti Scala'
VERSION = __version__

# Required packages
REQUIRED = [
    'MechanicalSoup'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*", "dist", "*.egg-info"]),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7'
        ]
)
