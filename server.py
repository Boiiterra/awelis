from flask import Flask
from logging import getLogger

from parser import parser


Page = str
app = Flask(__name__, static_url_path='/static')
log = getLogger('werkzeug')
log.disabled = True


def get_page() -> Page:
    data = None

    with open("./page.html", "r") as file:
        data = file.read()

    with open("./main.js") as file:
        js = file.read()

    if data:
        data = data.replace("<!--jscode-->", js)

    return data


def in_data_page(data: str, page: Page) -> Page:
    return page.replace("<!--data-->", data)


@app.route("/", methods=['GET'])
def show() -> Page:
    page = get_page()
    if (page is None):
        page = "<!--data-->"

    data = "<h1>No file is currently being watched</h1>"

    try:
        file = open("./.env", "r")
        tmp = file.readline()  # I read one line cuz there is only one line
        if ("FILE=" in tmp):
            nfile = tmp.split("=")[1].replace("'", "").replace("\n", "")
        else:
            raise Exception("Cursor is not set yet. Please use updater")

        file.close()
        file = open(nfile, "r")
        data = file.read()
        data = parser(data)

        file.close()
    except Exception as e:
        print(e)

    data = in_data_page(data, page)

    return data


@app.route("/reload")
def reloader():
    with open(".env") as file:
        _ = file.readline()  # ignore first line
        status = file.readline().split(
            "=")[1].replace("'", "").replace("\n", "")

    if (status == "True"):
        with open(".env", "r") as file:
            old = file.read().split("\n")

        with open(".env", "w") as file:
            old[1] = "RELOAD='False'"
            file.write("\n".join(old))

    # TODO: Add file edit time status

    return status


def start_server():
    app.run(port=6969)


if __name__ == "__main__":
    print("Usage: ./start.py")
