import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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


class TestTextNodeToHTMLNode(unittest.TestCase):
    """Tests for the text_node_to_html_node function."""

    def test_text(self):
        """Test conversion of a plain text node."""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        """Test conversion of a bold text node."""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        """Test conversion of an italic text node."""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        """Test conversion of a code snippet text node."""
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")

    def test_link(self):
        """Test conversion of a hyperlink text node."""
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        """Test conversion of an image text node."""
        node = TextNode("An image", TextType.IMAGE,
                        "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
                         "src": "https://example.com/image.png", "alt": "An image"})

    def test_invalid_type(self):
        """Test conversion of an invalid text node type raises ValueError."""
        node = TextNode("Invalid", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
