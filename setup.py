#!/usr/bin/env python
# coding: utf-8
"""
Cloudflare Firewall Rules
-------------------------
Cloudflare Firewall Rules is a wrapper library that aims to easily create, modify, delete rules. It also provides a way to import & export new rules in your domain's firewall.

If you have several rules that you want to duplicate among your domains, this module is made for you!

Links:
* documentation
    <https://github.com/QuentiumYT/Cloudflare-Firewall-Rules/blob/main/README.md>
* online api documentation
    <https://quentiumyt.github.io/Cloudflare-Firewall-Rules/>
"""

from setuptools import setup

with open("cf_rules/__init__.py", "r") as file:
    VERSION = [x.split("=")[1].strip().strip('"') for x in file.readlines() if "__version__" in x][0]

with open("README.md", "r", encoding="utf-8") as file:
    README = file.read()

setup(
    name="cf-rules",
    version=VERSION,
    url="https://github.com/QuentiumYT/Cloudflare-Firewall-Rules",
    license="Apache 2.0",
    author="Quentin Lienhardt",
    author_email="pro@quentium.fr",
    description=("Wrapper library to import / export multiple remote rules "
                 "and easily create, modify and delete rules."),
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["cf_rules"],
    py_modules=["cf_rules.cf", "cf_rules.utils"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.27",
        "sphinx>=4.4",
        "sphinx-rtd-theme>=1.0",
        "sphinx-copybutton>=0.5",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
