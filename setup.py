#!/usr/bin/env python

from setuptools import setup

setup(name='CP',
      version='1.0',
      description='Automatic GUI-maker for hardware interface classes',
      author='Justin Lazear',
      author_email='jlazear@gmail.com',
      url='https://github.com/jlazear/cp',
      py_modules=['cp',],
      packages=['gui'],
      install_requires=['PyOscope', 'wxpython'],
      )