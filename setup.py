import re
import ast
import pip.download
from pip.req import parse_requirements
from setuptools import setup, find_packages


requirements = list(parse_requirements('requirements.txt', session=pip.download.PipSession()))

install_requires = [str(r.req) for r in requirements]

setup(
    name='dto-digitalmarketplace-apiclient',
    version='6.12.2',
    url='https://github.com/AusDTO/dto-digitalmarketplace-apiclient',
    license='MIT',
    author='GDS Developers',
    description='Digital Marketplace Data and Search API clients',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires
)
