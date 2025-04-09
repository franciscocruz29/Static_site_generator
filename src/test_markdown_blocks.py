import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_blocks(self):
        """Blocks should be split by double newlines, and each trimmed."""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_blank_lines(self):
        """Multiple consecutive blank lines should not create empty blocks."""
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        """Whitespace around blocks should be trimmed."""
        md = """


   # Heading

   Paragraph with text

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph with text"
            ]
        )

    def test_empty_string(self):
        """An empty string should return an empty list."""
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_blank_lines(self):
        """A string with only newlines or whitespace should return an empty list."""
        md = "\n\n   \n\n\t\n"
        self.assertEqual(markdown_to_blocks(md), [])

    def test_single_block(self):
        """A single block of text should be returned as a one-element list."""
        md = "Just a single paragraph"
        self.assertEqual(markdown_to_blocks(md), ["Just a single paragraph"])


if __name__ == "__main__":
    unittest.main()
