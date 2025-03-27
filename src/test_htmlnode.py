import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_initialization(self):
        """Test various ways of initializing an HTMLNode"""
        # Full initialization
        node1 = HTMLNode(
            tag="div",
            value="Hello World",
            children=None,
            props={"class": "container"}
        )
        self.assertEqual(node1.tag, "div")
        self.assertEqual(node1.value, "Hello World")
        self.assertIsNone(node1.children)
        self.assertEqual(node1.props, {"class": "container"})

        # Minimal initialization
        node2 = HTMLNode()
        self.assertIsNone(node2.tag)
        self.assertIsNone(node2.value)
        self.assertIsNone(node2.children)
        self.assertIsNone(node2.props)

    def test_props_to_html(self):
        """Test HTML properties conversion"""
        # Single property
        node1 = HTMLNode(props={"class": "test"})
        self.assertEqual(node1.props_to_html(), ' class="test"')

        # Multiple properties
        node2 = HTMLNode(props={
            "class": "container",
            "id": "main",
            "data-test": "value"
        })
        props_html = node2.props_to_html()
        self.assertIn(' class="container"', props_html)
        self.assertIn(' id="main"', props_html)
        self.assertIn(' data-test="value"', props_html)

        # No properties
        node3 = HTMLNode()
        self.assertEqual(node3.props_to_html(), "")

    def test_repr_method(self):
        """Test string representation of HTMLNode"""
        node = HTMLNode(
            tag="p",
            value="Test",
            children=None,
            props={"class": "paragraph"}
        )
        expected_repr = "HTMLNode(p, Test, children: None, {'class': 'paragraph'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_not_implemented(self):
        """Verify to_html method raises NotImplementedError"""
        node = HTMLNode(tag="div", value="Test")
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leafnode_initialization(self):
        """Test LeafNode initialization"""
        # Basic initialization
        node1 = LeafNode("p", "Hello World")
        self.assertEqual(node1.tag, "p")
        self.assertEqual(node1.value, "Hello World")
        self.assertIsNone(node1.children)
        self.assertIsNone(node1.props)

        # With properties
        node2 = LeafNode(
            "a",
            "Click here",
            {"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(node2.tag, "a")
        self.assertEqual(node2.value, "Click here")
        self.assertEqual(
            node2.props, {"href": "https://example.com", "target": "_blank"})

    def test_leafnode_value_required(self):
        """Verify that LeafNode requires a value"""
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leafnode_to_html(self):
        """Test HTML generation for different scenarios"""
        # No tag
        node1 = LeafNode(None, "Plain text")
        self.assertEqual(node1.to_html(), "Plain text")

        # With tag, no properties
        node2 = LeafNode("p", "Paragraph text")
        self.assertEqual(node2.to_html(), "<p>Paragraph text</p>")

        # With tag and properties
        node3 = LeafNode(
            "a",
            "Link",
            {"href": "https://example.com", "class": "external"}
        )
        self.assertEqual(
            node3.to_html(),
            '<a href="https://example.com" class="external">Link</a>'
        )

    def test_leafnode_special_characters(self):
        """Test handling of special characters"""
        node = LeafNode("div", "Text with <special> & characters")
        self.assertEqual(
            node.to_html(),
            '<div>Text with <special> & characters</div>'
        )

    def test_leafnode_empty_string_props(self):
        """Test LeafNode with empty string properties"""
        node = LeafNode("input", "", {"type": "text", "name": "username"})
        self.assertEqual(
            node.to_html(),
            '<input type="text" name="username"></input>'
        )

    def test_leafnode_repr(self):
        """Test string representation of LeafNode"""
        node = LeafNode("span", "Test", {"class": "highlight"})
        expected_repr = "LeafNode(span, Test, {'class': 'highlight'})"
        self.assertEqual(repr(node), expected_repr)


class TestParentNode(unittest.TestCase):
    def test_basic_parent_node(self):
        """Test a ParentNode with a single LeafNode child"""
        node = ParentNode("div", [LeafNode("span", "Hello")])
        self.assertEqual(node.to_html(), "<div><span>Hello</span></div>")

    def test_nested_parent_nodes(self):
        """Test ParentNode containing another ParentNode with children"""
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [LeafNode("p", "Paragraph inside section")]
                ),
                LeafNode("h1", "Heading")
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p>Paragraph inside section</p></section><h1>Heading</h1></div>"
        )

    def test_multiple_children(self):
        """Test ParentNode with multiple LeafNode children"""
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2"),
                LeafNode("li", "Item 3"),
            ]
        )
        self.assertEqual(
            node.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

    def test_no_tag_raises_error(self):
        """Test that ParentNode without a tag raises ValueError"""
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("p", "Content")])
        self.assertEqual(str(context.exception), "invalid HTML: no tag")

    def test_no_children_raises_error(self):
        """Test that ParentNode without children raises ValueError"""
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertEqual(str(context.exception),
                         "invalid HTML: no children")

    def test_empty_children_list(self):
        """Test ParentNode with an empty list of children"""
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_with_attributes(self):
        """Test ParentNode with HTML attributes (props)"""
        node = ParentNode("a", [LeafNode(None, "Click me")], {
                          "href": "https://example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://example.com">Click me</a>')

    def test_mixed_children_types(self):
        """Test ParentNode containing both LeafNode and nested ParentNode children"""
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, "Normal"),
                ParentNode(
                    "p",
                    [LeafNode(None, "Inside paragraph")]
                ),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><b>Bold</b>Normal<p>Inside paragraph</p></div>"
        )

    def test_special_characters(self):
        """Test handling of special characters like <, >, and & in text"""
        node = ParentNode(
            "p", [LeafNode(None, "Text with <, >, and & symbols")])
        self.assertEqual(
            node.to_html(), "<p>Text with <, >, and & symbols</p>")

    def test_deeply_nested_structure(self):
        """Test deeply nested ParentNodes to ensure recursion works properly"""
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "article",
                            [
                                LeafNode("h1", "Nested Heading"),
                                LeafNode("p", "Nested Paragraph")
                            ]
                        )
                    ]
                )
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><article><h1>Nested Heading</h1><p>Nested Paragraph</p></article></section></div>"
        )


if __name__ == "__main__":
    unittest.main()
