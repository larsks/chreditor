#!/usr/bin/env python

from distutils.core import setup

setup(name='chreditor',
      version='1.0',
      description='Edit server for Chrome "Edit with Emacs" extension',
      author='Lars Kellogg-Stedman',
      author_email='lars@oddbit.com',
      url='http://github.com/larsks/chreditor',
      py_modules=['chreditor'],
      install_requires=open('requirements.txt').readlines(),
      entry_points = {
          'console_scripts': [
                'chreditor = chreditor:main',
              ],
          }
     )

