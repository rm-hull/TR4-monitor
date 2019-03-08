#!/usr/bin/env python

from setuptools import setup

import beebeelog

setup(name='TR4-Monitor',
      version=tr4_monitor.__version__,
      description="A broadband speedtest data logger",
      url='http://github.com/rm-hull/TR4-monitor',
      author='Richard Hull',
      author_email="richard.hull@destructuring-bind.org",
      license='MIT',
      packages=['tr4_monitor'],
      install_requires=['requests', 'speedtest-cli'],
      zip_safe=False)
