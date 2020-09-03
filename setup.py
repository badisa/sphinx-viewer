import re
import ast

from setuptools import setup, find_packages

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("sphinxviewer/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

setup(
    name="sphinx-viewer",
    version=version,
    packages=find_packages(),
    url="http://www.eyesopen.com",
    author="Forrest York",
    author_email="oews@eyesopen.com",
    description="A browser based sphinx editor that allows for building while editing",
    long_description=open("README.md").read(),
    zip_safe=False,
    license="MIT",
    keywords="sphinx browser",
    entry_points={"console_scripts": ["sphinx-viewer = sphinxviewer.main:main"]},
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Sphinx",
        "Topic :: Documentation :: Sphinx",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
