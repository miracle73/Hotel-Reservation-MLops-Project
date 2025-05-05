from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="HOTEL RESERVATION ML PROJECT",
    version="0.1.0",
    author="mirack",
    packages=find_packages(),
    install_requires = requirements,

)