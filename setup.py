#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name='gcfilter',
        version='0.1',
        packages=find_packages(),
        install_requires=['biopython', 'docopt'],

        author='Dillon Barker',
        author_email='dillon.barker@canada.ca',
        description='Filters FASTQ files on GC content',
        license='GPL 3+',
        keywords='bioinformatics fastq sequence',
        url='https://github.com/dorbarker/gcfilter',

        entry_points={
            'console_scripts': [
                'gcfilter = gcfilter.gcfilter:main'
                ]}
)
