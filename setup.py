# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = open(os.path.join(here, 'requirements.txt')).readlines()

setup(
    name='feedduty',
    version='0.1.0-dev',
    description='Feed Duty',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Bastian Kuberek',
    author_email='bkuberek@gmail.com',
    url='https://github.com/bkuberek/feedduty',
    keywords='web wsgi bfg pylons pyramid feed',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='test',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = feedduty:main'
        ],
        'console_scripts': [
            'feedduty = feedduty.commands:main'
        ]
    }
)
