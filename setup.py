#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    # redditdb...
    # loggable...
    'flask', 'memoized_property',
]

PACKAGE_NAME = 'vortex'
setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    author="mvr",
    description="mirror and query URLs entered into slack with redditdb",
    author_email='no-reply@example.com',
    url='https://github.com/mattvonrocketstein/vortex',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False,
    entry_points={
        'console_scripts':
        ['vortex = {0}.bin.main:entry'.format(PACKAGE_NAME), ]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
