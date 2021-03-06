#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

PACKAGE_NAME = 'vortex'
REQUIREMENTS = [
    'flask',
    'memoized_property',
    'python-dotenv',
    'redditdb==0.1.0',
    'slacks==0.1.0',
]
GITHUB_REQUIREMENTS = [
    'https://github.com/mattvonrocketstein/redditdb/archive/master.zip#egg=redditdb-0.1.0',
    'https://github.com/mattvonrocketstein/python-slacks/archive/master.zip#egg=slacks-0.1.0',
]
setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    author="mvr",
    description="mirror and query URLs entered into slack with redditdb",
    author_email='no-reply@example.com',
    url='https://github.com/mattvonrocketstein/vortex',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    dependency_links=GITHUB_REQUIREMENTS,
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
