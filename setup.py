from setuptools import setup
from setuptools import find_packages

setup(
    name="search-tool",
    description="Replacement for grep",
    long_description="Replacement for grep",
    version="1.0.0",
    url="",
    author="Lahiru Fernando",
    author_email="wlrfernando@outlook.com",
    scripts=["scripts/search-tool"],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[]
)
