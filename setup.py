from setuptools import setup

setup(
    name="firefox_open_tabs",
    version="0.1.0",
    packages=["firefox_open_tabs"],
    url="https://github.com/nelimee/firefox_open_tabs",
    license="CeCILL-B",
    author="Adrien Suau",
    author_email="adrien.suau@protonmail.com",
    description="Get information about currently opened tabs in Firefox",
    install_requires=["lz4"],
    extra_require={"dev": ["black"]},
    entry_points={"console_scripts": ["firotab = firefox_open_tabs:main"]},
)
