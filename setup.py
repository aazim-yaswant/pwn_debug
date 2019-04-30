#!/usr/bin/env python

from setuptools import setup

setup(name='pwn_debug',
    version="0.1",
    description='pwn_debug: easy to libc source code debug and make breakpoint',
    author='raycp',
    author_email='raycp@protonmail.com',
    maintainer='raycp',
    maintainer_email='raycp',
    url='ray-cp.github.io',
    packages=['pwn_debug'],
    install_requires=[
        'pwntools',
              ],
    long_description="easy to libc source code debug and make breakpoint.",
    license="Public domain",
    platforms=["any"],
    )
