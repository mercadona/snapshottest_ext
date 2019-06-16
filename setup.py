import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="snapshottest_ext",
    version="0.2.0",
    description="extra formatter for snapshottest",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/swuecho/snapshotest_ext",
    author="Hao Wu",
    author_email="echowuaho@foxmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["snapshottest"],
)
