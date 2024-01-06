from re import match, Match

markdown = str
html = str


class HeaderError(Exception):
    def __init__(self, header_type: int):
        super().__init__(
            f"Header {header_type} does not exist.\n"
            "Headers fall in range from 1 up to 6."
        )


def make_header(value: str, header_type: int) -> str:
    """Can raise an exception"""
    if header_type < 1 or header_type > 6:
        raise HeaderError(header_type)

    return f"<h{header_type}>{value[header_type + 1:]}</h{header_type}>"


def match_header(line: str, header_type: int) -> bool:
    """Can raise an exception"""
    if header_type < 1 or header_type > 6:
        raise HeaderError(header_type)

    reg = "#" * header_type + " .*"

    mtch = match(reg, line)
    return mtch


def parser(content: markdown) -> html:
    page = ""

    for line in content.split("\n"):
        if not len(line):  # ignore empty line
            continue

        matched: bool | Match = False

        # Headers
        header = line.count("#")
        if 1 <= header <= 6:
            matched = match_header(line, header)
            if isinstance(matched, Match):
                line = make_header(matched.group(0), header)

        if not matched:
            line = f"<p>{line}</p>"

        page += line + "\n"

    print(page)
    return page
