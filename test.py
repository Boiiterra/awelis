import unittest
from re import Match

from parser import parser, match_header, make_header, match_special_header, make_special_header, match_nline_par, HeaderError, InvalidMarkdown

# I don't know why I made those. But they do help a little :P


class TestWebmark(unittest.TestCase):
    def test_valid_header(self):
        for hl in range(1, 7):
            t = "#" * hl + " This is test header"
            self.assertEqual(make_header(t, hl),
                             f"<h{hl}>{t[hl + 1:]}</h{hl}>",
                             "Valid header is considered invalid!")

    def test_invalid_header(self):
        for hl in [n for n in range(-5, 10) if 1 > n or n > 6]:
            t = "# This is invalid but header_lvl is higher priority."
            with self.assertRaises(HeaderError):
                make_header(t, hl)

    def test_invalid_md_header(self):
        for hl in range(1, 7):
            t = "#" * hl + "Invalid header with valid amount of #"
            with self.assertRaises(InvalidMarkdown):
                make_header(t, hl)

        for hl in range(1, 7):
            t = "#" * (hl + 1) + " Valid header with invalid amount of #"
            with self.assertRaises(InvalidMarkdown):
                make_header(t, hl)

    def test_header_matcher_valid(self):
        for hl in range(1, 7):
            t = "#" * hl + " This is test header"
            self.assertIsInstance(match_header(t, hl), Match)

    def test_header_matcher_invalid(self):
        for hl in range(1, 7):
            t = "#" * (hl - 1) + " This is wrong test header"
            self.assertIsNone(match_header(t, hl))

        for hl in range(1, 7):
            t = "#" * (hl + 1) + " This is wrong test header"
            self.assertIsNone(match_header(t, hl))

        for hl in [n for n in range(-5, 10) if 1 > n or n > 6]:
            t = "# Invalid header level."
            with self.assertRaises(HeaderError):
                make_header(t, hl)

    def test_special_headers(self):
        with self.assertRaises(HeaderError):
            make_special_header("Hello\n-", 0)

        with self.assertRaises(HeaderError):
            make_special_header("Hello\n=", 10)

        header_txt = "I am just a header text with newline\n"
        header1 = match_special_header(header_txt + "=", 1)
        self.assertIsInstance(header1, Match)
        self.assertEqual(make_special_header(header1.group(1), 1),
                         f"<h1>{header_txt[:-1]}</h1>")

        header2 = match_special_header(header_txt + "-", 2)
        self.assertIsInstance(header2, Match)
        self.assertEqual(make_special_header(header2.group(1), 2),
                         f"<h2>{header_txt[:-1]}</h2>")

        line1 = "hello"
        line2 = "-"
        header = match_special_header(line1 + "\n" + line2, 2)
        self.assertIsInstance(header, Match)
        self.assertEqual(make_special_header(header.group(1), 2),
                         f"<h2>{line1}</h2>")

    def test_nline_paragraphs(self):
        par = "Some text"
        nline = "  \n"
        self.assertIsInstance(match_nline_par(par + nline), Match)
        nline = "      \n"
        self.assertIsInstance(match_nline_par(par + nline), Match)

        nline = " \\\n"
        mtch = match_nline_par(par + nline)
        self.assertIsInstance(mtch, Match)
        nline = "      \\\n"
        mtch = match_nline_par(par + nline)
        self.assertIsInstance(mtch, Match)

    def dont_test_parser(self):
        data = "# This is an error"
        with open("example.md") as file:
            data = file.read()

        print(parser(data))


if __name__ == "__main__":
    unittest.main()
