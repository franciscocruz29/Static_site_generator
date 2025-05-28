import unittest
from extract import extract_title


class TestExtract(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
        markdown = " # Hello "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
        markdown = "   # Hello   "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")


if __name__ == "__main__":
    unittest.main()
