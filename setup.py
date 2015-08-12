#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup package."""
from setuptools import setup, find_packages

LONG_DESC = '''
Subclrschm is a color scheme editor for Sublime Text.
It built with wxPython 2.9.4 and requires Python 2.7.

The project repo is found at:
https://github.com/facelessuser/ColorSchemeEditor.
'''

setup(
    name='subclrschm',
    version='1.0.0',
    keywords='Sublime color scheme',
    description='GUI for editing Sublime Text color schemes.',
    long_description=LONG_DESC,
    author='Isaac Muse',
    author_email='Isaac.Muse [at] gmail.com',
    url='https://github.com/facelessuser/ColorSchemeEditor',
    packages=find_packages(exclude=['pyinstaller*']),
    install_requires=[
    ],
    zip_safe=False,
    entry_points={
        'gui_scripts': [
            'subclrschm=subclrschm.__main__:main'
        ]
    },
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
