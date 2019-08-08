#!/bin/env python3
# -*- coding: utf-8 -*-

import configparser

# Standard
import json
import pathlib
import typing as typ

# Non-standard
import lz4.block as lz4


def _get_opened_tabs_from_json_recovery(
    recovery_json: typ.Dict[str, typ.Any]
) -> typ.List[typ.Dict[str, typ.Any]]:
    """Extract the currently opened tabs from the recovery.json data.

    :param recovery_json: A dictionary obtained from the json.load method of Python's json
        standard module. The file represented is recovery.jsonlz4 after uncompression.
    :return: a list containing all the opened tabs of all the opened Firefox instances.
    """
    opened_tabs = list()
    for window in recovery_json["windows"]:
        for tab in window["tabs"]:
            current_index = int(tab["index"]) - 1
            current_tab = tab["entries"][current_index]
            opened_tabs.append(current_tab)
    return opened_tabs


def get_current_opened_tab_information() -> typ.List[typ.Dict[str, typ.Any]]:
    """Recovers the currently opened tabs.

    :return: a list containing all the opened tabs of all the opened Firefox instances.
    """
    # First find the "recovery.jsonlz4" file by playing with paths.
    home_directory = pathlib.Path.home()
    firefox_directory = home_directory / ".mozilla" / "firefox"
    profiles_files = firefox_directory / "profiles.ini"

    profiles_config = configparser.ConfigParser()
    profiles_config.read(profiles_files)

    profile0_directory_name = profiles_config["Profile0"]["Path"]
    profile0_directory = firefox_directory / profile0_directory_name

    profile0_session_backup_directory = profile0_directory / "sessionstore-backups"
    compressed_recovery_file = profile0_session_backup_directory / "recovery.jsonlz4"

    # Read the "recovery.jsonlz4" by:
    #  1. Reading the header and checking its validity.
    #  2. Reading the leftover, decompressing, and interpreting it as a JSON text file.
    with open(compressed_recovery_file, "rb") as compf:
        assert compf.read(8) == b"mozLz40\0"
        compressed_recovery_json = compf.read()
    uncompressed_recovery_json = lz4.decompress(compressed_recovery_json)
    recovery_data = json.loads(uncompressed_recovery_json)

    tabs = _get_opened_tabs_from_json_recovery(recovery_data)
    return tabs


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Get information about currently opened Firefox tabs."
    )
    parser.add_argument(
        "--url",
        help="Filter output to print only opened tabs' URLs.",
        action="store_true",
    )
    parser.add_argument(
        "--title",
        help="Filter output to print only opened tabs' titles.",
        action="store_true",
    )
    args = parser.parse_args()

    if args.url and args.title:
        print("'--url' and '--title' options should not be used alongside.")
        exit()

    opened_tabs = get_current_opened_tab_information()
    if not args.url and not args.title:
        from pprint import pprint

        pprint(opened_tabs)
    elif args.url and not args.title:
        print("\n".join([tab["url"] for tab in opened_tabs]))
    elif args.title and not args.url:
        print("\n".join([tab["title"] for tab in opened_tabs]))


if __name__ == "__main__":
    main()
