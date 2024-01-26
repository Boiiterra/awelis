from re import fullmatch, Match

markdown = str
html = str


def make_header(md: markdown, header_lvl: int) -> str:
    return f"<h{header_lvl}>{md[header_lvl + 1:]}</h{header_lvl}>"


def match_header(line: str, header_lvl: int) -> Match | None:
    reg = "#" * header_lvl + " (.*)"

    mtch = fullmatch(reg, line)
    return mtch


def match_special_header(lines: str, header_lvl: int) -> Match | None:
    mtch = None

    if header_lvl == 1:
        mtch = fullmatch("(.+?)\n=+", lines)
    if header_lvl == 2:
        mtch = fullmatch("(.+?)\n-+", lines)

    return mtch


def make_special_header(source: markdown, header_lvl: int) -> html:
    if header_lvl == 1:
        return f"<h1>{source}</h1>"
    return f"<h2>{source}</h2>"


def match_nline_par(md: markdown) -> Match | None:
    return fullmatch("(.+?)  +\n", md) or fullmatch("(.+?)  *\\\\+\n", md)


def parser(content: markdown) -> html:
    page = ""
    file_content = content.split("\n")
    fct_len = len(file_content)

    line_ind = 0
    while line_ind < fct_len:
        line = file_content[line_ind]

        matched: Match | None = None

        # Headers
        header = line.count("#")
        if 1 <= header <= 6:
            matched = match_header(line, header)
            if isinstance(matched, Match):
                line = make_header(matched.group(0), header)

        # Special header cases
        if (line_ind + 1 < fct_len) and not matched:
            future_line = file_content[line_ind + 1]

            # Try header 1
            matched = match_special_header(line + "\n" + future_line, 1)
            if isinstance(matched, Match):
                line = make_special_header(matched.group(1), 1)
                line_ind += 1
            else:
                # Try header 2
                matched = match_special_header(line + "\n" + future_line, 2)
                if isinstance(matched, Match):
                    line = make_special_header(matched.group(1), 2)
                    line_ind += 1

        # Paragraph
        # TODO: Make better
        if not matched:
            matched = match_nline_par(line + "\n")
            if isinstance(matched, Match):
                line = f"{matched.group(1)}<br>"

        if not matched:
            line = f"{line} "

        line_ind += 1  # Move to the next line
        page += line + "\n"

    return page
