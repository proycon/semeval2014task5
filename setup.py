#!/usr/bin/env python
from setuptools import setup, find_packages
entry_points = {'console_scripts': [
    'semeval2014task5-setview = libsemeval2014task5.setview:main',
    'semeval2014task5-evaluate = libsemeval2014task5.evaluation:main',
    'semeval2014task5-manualsetbuild = libsemeval2014task5.manualsetbuild:main',
]}
setup(
    name = "libsemeval2014task5",
    version = "2.0",
    author = "Maarten van Gompel",
    author_email = "proycon@anaproy.nl",
    description = ("Library for SemEval 2014 task 5 - L2 Writing Assistant"),
    license = "GPL",
    keywords = "nlp computational_linguistics translation",
    long_description="Library for SemEval 2014 task 5 - L2 Writing Assistant",
    packages=['libsemeval2014task5'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    #include_package_data=True,
    #package_data = {'': ['*.wsgi','*.js','*.xsl','*.gif','*.png','*.xml','*.html','*.jpg','*.svg','*.rng'] },
    install_requires=['lxml >= 2.2'],
    entry_points = entry_points
)
