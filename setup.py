#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup package."""
from setuptools import setup, find_packages
import os
import imp
import traceback


def get_version():
    """Get version and version_info without importing the entire module."""

    devstatus = {
        'alpha': '3 - Alpha',
        'beta': '4 - Beta',
        'candidate': '4 - Beta',
        'final': '5 - Production/Stable'
    }
    path = os.path.join(os.path.dirname(__file__), 'subclrschm', 'lib')
    fp, pathname, desc = imp.find_module('__version__', [path])
    try:
        v = imp.load_module('__version__', fp, pathname, desc)
        return v.version, devstatus[v.version_info[3]]
    except Exception:
        print(traceback.format_exc())
    finally:
        fp.close()


VER, DEVSTATUS = get_version()

LONG_DESC = '''
Sublime Color Scheme Editor (subclrschm) is a color scheme editor for Sublime Text 3.

It is built with wxPython 4.0.0+ and requires Python 2.7 or 3.4+.
You can learn more about using subclrschm by `reading the docs`_.

.. _`reading the docs`: http://facelessuser.github.io/subclrschm/

Support
=======

Help and support is available here at the repository's `bug tracker`_.
Please read about `support and contributing`_ before creating issues.

.. _`bug tracker`: https://github.com/facelessuser/subclrschm/issues
.. _`support and contributing`: http://facelessuser.github.io/subclrschm/contributing/
'''

setup(
    name='subclrschm',
    version=VER,
    keywords='Sublime color scheme',
    description='GUI for editing Sublime Text color schemes.',
    long_description=LONG_DESC,
    author='Isaac Muse',
    author_email='Isaac.Muse@gmail.com',
    url='https://github.com/facelessuser/subclrschm',
    packages=find_packages(exclude=['tests', 'tools']),
    install_requires=[
        "wxpython>=4.0.0a3"
    ],
    zip_safe=False,
    entry_points={
        'gui_scripts': [
            'subclrschm=subclrschm.__main__:main'
        ]
    },
    package_data={
        'subclrschm.lib.gui.data': ['*.png', '*.ico', '*.icns']
    },
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
