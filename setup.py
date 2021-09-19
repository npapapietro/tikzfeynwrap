from setuptools import find_packages, setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    "docker_py>=1.10.6",
    "ipython>=7.27.0"
]

setup(
    name='tikzfeynwrap',
    version='0.1.0',
    description='Simple Wrapper for latex docker container',
    install_requires=install_requires,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    author="Nathan Papapietro <npapapietro95@gmail.com>",
    author_email="npapapietro95@gmail.com",
    url="https://github.com/npapapietro/tikzfeynwrap",
    classifiers=[
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)