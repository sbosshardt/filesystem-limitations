# Based on: https://packaging.python.org/tutorials/packaging-projects/

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filesystem-limitations-sbosshardt",
    version="0.0.1",
    author="Samuel Bosshardt",
    author_email="support@sbosshardt.com",
    description="A cross-platform Python library providing a simple way to determine filesystem limitations of a given directory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sbosshardt/filesystem-limitations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: System :: Filesystems",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: Jython",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha"
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: POSIX",
    ],
    # TBD: Should this version number be adjusted up/down?
    python_requires='>=2.6',
)