# coding: utf-8
from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages


setup(
    name='9cumber server',
    author='Yuki Mukasa',
    author_email='info@arg.vc',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    license='MIT'
)
