# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='padlang',
    version='1.0.4',
    description='PADLang is yet another interpreted language now with focus on Pascal/C-like syntax',
    long_description=long_description,
    url='https://github.com/zaklaus/padlang',
    author='Dominik Madarasz',
    author_email='zaklaus@madaraszd.net',
    license='Apache 2.0',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Other',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='interpreted development language pascal c',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'samples', 'tests']),
    #install_requires=['peppercorn'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={

    },
    data_files=[],
    entry_points={
        'console_scripts': [
            'pad=pad:main',
        ],
    },
    include_package_data=True
)
