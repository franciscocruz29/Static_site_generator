import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

# All tests functions and file names must start with test_ to be discoverable by unittest


class TestTextNode(unittest.TestCase):
    """Tests for the TextNode class and its methods."""

    def test_eq(self):
        """Test that two TextNode instances with the same text, type, and URL are equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        """Test that two TextNode instances with the same text, type, and identical URLs are equal."""
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        """Test that two TextNode instances with different text but the same type are not equal."""
        node = TextNode("Text node 1", TextType.TEXT)
        node2 = TextNode("Text node 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        """Test that two TextNode instances with the same text but different types are not equal."""
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        """Test that two TextNode instances with the same text and type but different URLs are not equal."""
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK,
                         "https://another-example.com")
        self.assertNotEqual(node, node2)

    def test_eq_both_urls_none(self):
        """Test that two TextNode instances with identical text, type, and both URLs as None are equal."""
        node = TextNode("Code block", TextType.CODE, None)
        node2 = TextNode("Code block", TextType.CODE, None)
        self.assertEqual(node, node2)

    def test_not_eq_one_url_none(self):
        """Test that a TextNode with a URL is not equal to another with None as the URL."""
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        """Test the __repr__ method of TextNode to ensure correct string representation."""
        node = TextNode("Test node", TextType.BOLD, "https://example.com")
        expected = "TextNode(Test node, bold, https://example.com)"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
