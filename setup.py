# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages


setup(
    name='cucumber',
    author='Yuki Mukasa',
    author_email='info@arg.vc',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    license='MIT'
)
