#!/usr/bin/env python3

"""Do not import it. It is a standalone file.
    Run it for the first time to see how to use it"""

from sys import argv
from os.path import isfile


def help():
    print("Help message")
    print(f"Usage: {argv[0]} <filepath to markdown file>")
    print(f"{argv[0]} -h     \\")
    print(f"{argv[0]} h      |-> to print this")
    print(f"{argv[0]} --help |->    message")
    print(f"{argv[0]} help   /")
    print("Markdown file must contain valid markdown code in "
          "order to be displayed properly.")
    print("And also filepath must be valid. Invalid filepath is not good.")
    print("This little program doesn't support multiple files.")


if (len(argv) == 2) and (argv[1] not in ["-h", "h", "--help", "help"]):
    filepath = argv[1]
    print(f"Setting cursor to file {filepath}")

    if isfile(filepath):
        print(f"New cursor is set. Target: {filepath}")
        try:
            file = open("./.env", "w")
            file.write(f"FILE={filepath}")
        except Exception as e:
            print("Failed to update cursor.")
            print(e)

    else:
        print(f"Provided path is invalid there is no file: {filepath}")
        exit(1)

    exit(0)

help()
