import unittest
from textnode import TextNode, TextType

# All tests functions and file names must start with test_ to be discoverable by unittest


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("Text node 1", TextType.NORMAL)
        node2 = TextNode("Text node 2", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK,
                         "https://another-example.com")
        self.assertNotEqual(node, node2)

    def test_eq_both_urls_none(self):
        node = TextNode("Code block", TextType.CODE, None)
        node2 = TextNode("Code block", TextType.CODE, None)
        self.assertEqual(node, node2)

    def test_not_eq_one_url_none(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Test node", TextType.BOLD, "https://example.com")
        expected = "TextNode(Test node, bold, https://example.com)"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
