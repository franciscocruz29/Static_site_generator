import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    """Tests for inline markdown processing functions."""

    # --- Tests for split_nodes_delimiter ---

    def test_delim_bold(self):
        """Tests for bold formatting using ** delimiter."""
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        """Tests multiple bolded words in a sentence using ** delimiter."""
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        """Tests bold formatting for multiple words using ** delimiter."""
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        """Tests italic formatting using _ delimiter."""
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        """Tests bold and italic formatting together using ** and _ delimiters."""
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        """Tests inline code formatting using ` delimiter."""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_unmatched(self):
        """Tests behavior when delimiters are not properly closed."""
        node = TextNode("This is an *italic sentence", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_delim_adjacent(self):
        """Tests adjacent formatted sections without spaces."""
        node = TextNode("**bold**_italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_nested(self):
        """Tests behavior with nested formatting, which should not be parsed incorrectly."""
        node = TextNode("This is **bold and _italic_** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                # Nested case should not be split
                TextNode("bold and _italic_", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    # --- Tests for extract_markdown_images ---

    def test_extract_images_single(self):
        """Tests extracting a single markdown image."""
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images_multiple(self):
        """Tests extracting multiple markdown images."""
        text = "![img1](url1.png) and ![img2](url2.jpg) and text ![img3](url3.gif)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("img1", "url1.png"), ("img2", "url2.jpg"),
             ("img3", "url3.gif")], matches
        )

    def test_extract_images_none(self):
        """Tests text with no markdown images."""
        text = "This text has no images, maybe a [link](here.com)?"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    # --- Tests for extract_markdown_links ---

    def test_extract_links_single(self):
        """Tests extracting a single markdown link."""
        text = "This is text with a [link](https://www.google.com)."
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_links_multiple(self):
        """Tests extracting multiple markdown links."""
        text = "Text with [link1](url1) and [link2](url2)."
        matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)

    def test_extract_links_none(self):
        """Tests text with no markdown links."""
        text = "This text has no links."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()
