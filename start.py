#!/usr/bin/env python3

from webbrowser import open as url_open
from multiprocessing import Process
from os import devnull
from time import sleep
import sys

from server import start_server

print("It is recommended to start this file in backgound.")

CPS = 10  # Checks per second


# https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


server = Process(target=start_server)
browser = Process(target=url_open, args=['localhost:6969', 1])

print("Starting server. All output from server is disabled.")
with HiddenPrints():
    server.start()

print("Launching new browser window for live preview.")
browser.start()

print("Browser tab will close automatically if server is down.")

while server.is_alive():
    with open("./.env") as file:
        l1 = file.readline()
        l2 = file.readline()
        data = file.readline().replace("\n", "").replace("'", "")

    if data == "CLOSE=True":
        server.terminate()

        with open("./.env", "w") as file:
            file.write(l1 + l2 + "CLOSE='False'\n")
        break

    sleep(1 / CPS)
