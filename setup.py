#! /usr/bin/env python

import setuptools

with open('requirements.txt', 'rt', encoding='ascii') as f:
    requirements = f.readlines()

setuptools.setup(
        name = 'slidetextbridge',
        version='0.1.0',
        package_dir={'': 'src'},
        packages=setuptools.find_packages(where='src'),
        install_requires=requirements,
        entry_points={
            'console_scripts': [
                'slidetextbridge=slidetextbridge.core.main:main',
            ],
        }
)
