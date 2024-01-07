import unittest
from re import Match

from parser import match_header, make_header, HeaderError, InvalidMarkdown


class TestWebmark(unittest.TestCase):
    def test_valid_header(self):
        for ht in range(1, 7):
            t = "#" * ht + " This is test header"
            self.assertEqual(make_header(t, ht),
                             f"<h{ht}>{t[ht + 1:]}</h{ht}>",
                             "Valid header is considered invalid!")

    def test_invalid_header(self):
        for ht in [n for n in range(-5, 10) if 1 > n or n > 6]:
            t = "# This is invalid but header_lvl is higher priority."
            with self.assertRaises(HeaderError):
                make_header(t, ht)

    def test_invalid_md_header(self):
        for ht in range(1, 7):
            t = "#" * (ht+1) + " Invalid header with valid amount of #"
            with self.assertRaises(InvalidMarkdown):
                make_header(t, ht)

        for ht in range(1, 7):
            t = "#" * (ht + 1) + " Valid header with invalid amount of #"
            with self.assertRaises(InvalidMarkdown):
                make_header(t, ht)

    def test_header_matcher_valid(self):
        for ht in range(1, 7):
            t = "#" * ht + " This is test header"
            self.assertIsInstance(match_header(t, ht), Match)

    def test_header_matcher_invalid(self):
        for ht in range(2, 8):
            t = "#" * ht + " This is wrong test header"
            self.assertIsNone(match_header(t, ht))

        for ht in range(0, 6):
            t = "#" * ht + " This is wrong test header"
            self.assertIsNone(match_header(t, ht))

        for ht in [n for n in range(-5, 10) if 1 > n or n > 6]:
            t = "# Invalid header level."
            with self.assertRaises(HeaderError):
                make_header(t, ht)


if __name__ == "__main__":
    unittest.main()
