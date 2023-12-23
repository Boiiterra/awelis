#!/usr/bin/env python3

"""Do not import it. It is a standalone file.
   Run it for the first time to see how to use it"""

from sys import argv
from os.path import isfile


def help():
    print("Help message")
    print("Usage: argv[0]")
    print(" <markdown file> -> set cursor to file")
    print(" -h, --help      -> to print this message")
    print(" -s, --stop      -> to stop server")
    print("\nMarkdown file must contain valid markdown code in "
          "order to be displayed properly.")
    print("And also filepath must be valid. Invalid filepath is not good.")
    print("This little program doesn't support multiple files.")


closing = ["-s", "--stop"]
flags = ["-h", "--help"] + closing

if (len(argv) == 2) and (argv[1] not in flags):
    filepath = argv[1]
    print(f"Setting cursor to file {filepath}")

    if isfile(filepath):
        print(f"New cursor is set. Target: {filepath}")
        try:
            file = open("./.env", "r")
            file.readline()
            file.readline()
            l3 = file.readline()
            file.close()

            file = open("./.env", "w")
            file.write(f"FILE='{filepath}'\n" + "RELOAD='True'\n" + l3)

        except Exception as e:
            print("Failed to update cursor.")
            print(e)
        finally:
            file.close()

    else:
        print(f"Provided path is invalid there is no file: {filepath}")
        exit(1)

    exit(0)

if (len(argv) == 2 and (argv[1]) in closing):
    with open("./.env") as file:
        l1 = file.readline()
        l2 = file.readline()

    with open("./.env", "w") as file:
        file.write(l1 + l2 + "CLOSE='True'\n")

    print("Server will close shortly.")

    exit(0)


help()
