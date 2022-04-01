"""Setup for packaging."""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='quibble',
    version='0.0.1dev',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/KarlSchwenk/quibble',
    license='LGPL-2.1',
    author='KarlSchwenk',
    author_email='km.schwenk@web.de',
    description='Framework for Various Optimization Tasks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy==1.18.5']
)
