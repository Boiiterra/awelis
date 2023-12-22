class markdown(str):
    """Just a fancy name for str"""
    pass


class html(str):
    """Just a fancy name for str"""
    pass


def __sur_h(value: str, header_type: int) -> [str, bool]:
    return f"<h{header_type}>{value[header_type + 1:]}</h{header_type}>", True


def parser(content: markdown) -> html:
    page = ""

    for line in content.split("\n"):
        if not len(line):  # ignore empty line
            continue

        matched = False

        # Headers
        match line.split()[0]:
            case "#": line, matched = __sur_h(line, 1)
            case "##": line, matched = __sur_h(line, 2)
            case "###": line, matched = __sur_h(line, 3)
            case "####": line, matched = __sur_h(line, 4)
            case "#####": line, matched = __sur_h(line, 5)
            case "######": line, matched = __sur_h(line, 6)

        page += "<p>" * (not matched) + line + "</p>" * (not matched)

    return page
