import re
import ast
from setuptools import setup, find_packages

setup(
    name='dto-digitalmarketplace-apiclient',
    version='6.12.3',
    url='https://github.com/AusDTO/dto-digitalmarketplace-apiclient',
    license='MIT',
    author='GDS Developers',
    description='Digital Marketplace Data and Search API clients',
    long_description=__doc__,
    packages=['dmapiclient'],
    include_package_data=True,
    install_requires=[
        'backoff',
        'Flask',
        'six',
        'requests',
        'enum34',
        'monotonic'
    ]
)
