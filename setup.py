#!/usr/bin/env python

from setuptools import setup

setup(name='CP',
      version='1.0',
      description='Automatic GUI-maker',
      author='Justin Lazear',
      author_email='jlazear@gmail.com',
      url='http://www.github.com/jlazear/cp',
      py_modules=['cp',],
      packages=['gui'],
      install_requires=['pyoscope>=1.0'],
      dependency_links=['https://github.com/jlazear/pyoscope/tarball/master']
      )