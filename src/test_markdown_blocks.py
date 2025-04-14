import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


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


class TestMarkdownBlockTypes(unittest.TestCase):
    """
    Test suite for the markdown block type detection functionality.
    Tests various markdown block types to ensure they are correctly identified.
    """

    def test_heading_blocks(self):
        """Test detection of heading blocks with different heading levels."""
        test_cases = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_invalid_heading_blocks(self):
        """Test blocks that look similar to headings but aren't valid headings."""
        test_cases = [
            "#Heading without space",
            "####### Too many hash symbols",
            "# \nHeading with newline"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        """Test detection of code blocks with varying content."""
        test_cases = [
            "```\nSimple code\n```",
            "```python\ndef function():\n    pass\n```",
            "```\n\n```"  # Empty code block
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_invalid_code_blocks(self):
        """Test blocks that look similar to code blocks but aren't valid."""
        test_cases = [
            "```\nMissing closing backticks",
            "Missing opening backticks\n```",
            "`` Not enough backticks ``"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_quote_blocks(self):
        """Test detection of quote blocks with varying content."""
        test_cases = [
            "> Single line quote",
            "> Multi-line\n> quote block",
            ">\n> Quote with empty line"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_invalid_quote_blocks(self):
        """Test blocks that are not valid quote blocks."""
        test_cases = [
            "> Quote start\nNon-quote line",
            "Not a quote"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_unordered_list_blocks(self):
        """Test detection of unordered list blocks."""
        test_cases = [
            "- Single item",
            "- Item 1\n- Item 2\n- Item 3",
            "- Item with\n- multiple\n- elements"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_invalid_unordered_list_blocks(self):
        """Test blocks that are not valid unordered lists."""
        test_cases = [
            "- Item 1\nNot a list item",
            "-Not a list item (no space)",
            "* Different marker"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_ordered_list_blocks(self):
        """Test detection of ordered list blocks."""
        test_cases = [
            "1. Single item",
            "1. Item 1\n2. Item 2\n3. Item 3",
            "1. First\n2. Second\n3. Third\n4. Fourth"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_invalid_ordered_list_blocks(self):
        """Test blocks that are not valid ordered lists."""
        test_cases = [
            "1. Item 1\nNot a list item",
            "1. Item 1\n3. Missing number 2",
            "2. Doesn't start with 1",
            "1.No space after period"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_paragraph_blocks(self):
        """Test detection of paragraph blocks."""
        test_cases = [
            "Simple paragraph",
            "Paragraph with\nmultiple lines",
            "Paragraph with\n\nblank lines"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_edge_cases(self):
        """Test edge cases like empty blocks or special characters."""
        test_cases = [
            "",  # Empty block
            " ",  # Just whitespace
            "#",  # Just a hash
            "```",  # Single backtick line
            ">"  # Just a quote marker
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
