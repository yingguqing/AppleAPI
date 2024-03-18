#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = '影孤清'
"""

from pathlib import Path

from setuptools import find_packages
from setuptools import setup

README = Path(__file__).resolve().with_name("README.md").read_text()

print("{} - {}".format("*" * 10, find_packages()))

setup(
    name='AppleAPI',  # 包名字
    version='1.0.4',  # 包版本
    author='影孤清',  # 作者
    author_email='yingguqing@163.com',  # 作者邮箱
    keywords='ios apple appstore app store connect api appstoreconnectapi',
    description='App Store Connect API',  # 简单描述
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/yingguqing/AppleAPI',  # 包的主页
    packages=find_packages(),  # 包
    install_requires=['PyJWT~=2.0', 'pyOpenSSL>=20.0.0', 'requests~=2.20'],
    python_requires="~=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

