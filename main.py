from flask import Flask

from parser import parser


class Page(str):
    """This is like a string but for visual purposes"""
    pass


app = Flask(__name__)
filepath = "./.env"


def get_page() -> Page:
    data = None

    with open("./page.html", "r") as file:
        data = file.read()

    return data


def in_data_page(data: str, page: Page) -> Page:
    return page.replace("<!--data-->", data)


@app.route("/")
def show() -> Page:
    page = get_page()
    if (page is None):
        page = "<!--data-->"

    data = "<h1>No file is currently being watched</h1>"

    try:
        file = open("./.env", "r")
        tmp = file.readline()  # I read one line cuz there is only one line
        if ("FILE=" in tmp):
            nfile = tmp.split("=")[1]
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


if __name__ == "__main__":
    app.run(debug=True, port=6969)
