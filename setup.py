from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="firefox_open_tabs",
    version="0.1.0",
    description="Get information about currently opened tabs in Firefox",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["firefox_open_tabs"],
    url="https://github.com/nelimee/firefox_open_tabs",
    license="CeCILL-B",
    author="Adrien Suau",
    author_email="adrien.suau@protonmail.com",
    install_requires=["lz4"],
    extras_require={"dev": ["black", "setuptools", "wheel", "twine"]},
    entry_points={
        "console_scripts": ["firotab = firefox_open_tabs.firefox_open_tabs:main"]
    },
)
