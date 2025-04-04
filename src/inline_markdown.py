import re
from textnode import TextNode, TextType
from typing import List, Tuple


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """
    Splits text nodes by a specified delimiter and applies a given text type to the delimited sections.

    This function processes a list of text nodes and identifies occurrences of a delimiter within plain text.
    It splits the text at each delimiter, alternating between normal text and formatted text based on the
    specified text type. Non-plain-text nodes are preserved as-is.

    The function assumes that delimiters are properly balanced. If an unmatched delimiter is encountered,
    it raises a ValueError.

    Args:
        old_nodes (List[TextNode]): List of text nodes to process.
        delimiter (str): Delimiter that marks the beginning and end of a formatted section.
        text_type (TextType): Type to assign to the delimited (formatted) text sections.

    Returns:
        List[TextNode]: A new list of text nodes with sections correctly split and typed.

    Raises:
        ValueError: If the delimiters are unbalanced (i.e., an odd number of delimiter occurrences).

    Example:
        >>> node = TextNode("This is text with a `code block` word", TextType.TEXT)
        >>> split_nodes_delimiter([node], "`", TextType.CODE)
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
    """

    new_nodes = []

    for node in old_nodes:
        # Preserve non-plain-text nodes without changes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the text at each delimiter occurrence
        sections = node.text.split(delimiter)

        # Ensure delimiters are balanced (odd number of sections)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown: Unmatched delimiter found")

        # Iterate through the split sections
        for index, section in enumerate(sections):
            if section:
                if index % 2 == 0:
                    # Even index: plain (unformatted) text
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    # Odd index: text within delimiters, apply specified text type
                    new_nodes.append(TextNode(section, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extracts all image references from a Markdown-formatted string.

    Args:
        text (str): A string containing Markdown content.

    Returns:
        List[Tuple[str, str]]: A list of (alt_text, image_url) tuples for each image found.

    Example:
        >>> text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        >>> extract_markdown_images(text)
        [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]
    """
    # Regex pattern to match Markdown image syntax: ![alt text](image_url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extracts all standard markdown hyperlinks from the input text, excluding image links.

    Args:
        text (str): A string containing markdown-formatted content.

    Returns:
        List[Tuple[str, str]]: A list of tuples, where each tuple consists of:
            - anchor_text (str): The clickable text of the link.
            - link_url (str): The URL the anchor text points to.

    Example:
        >>> text = "Check out [Boot.dev](https://www.boot.dev) for coding tutorials."
        >>> extract_markdown_links(text)
        [('Boot.dev', 'https://www.boot.dev')]
    """
    # Regex pattern to match markdown links [text](url), excluding image links (![text](url))
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(pattern, text)
    return matches


def split_nodes_by_markdown_pattern(old_nodes: List[TextNode], pattern_type: str, extractor_func, node_type: TextType):
    """
    Splits text nodes by a given markdown pattern (e.g., links or images),
    extracting matched patterns into separate nodes.

    Args:
        old_nodes (list): List of TextNode objects to process.
        pattern_type (str): A label for the pattern type, used in error messages.
        extractor_func (callable): A function that extracts (text, url) tuples from a string.
        node_type (TextType): The type to assign to extracted markdown patterns
                              (e.g., TextType.LINK or TextType.IMAGE).

    Returns:
        list: A new list of TextNode objects, where matched patterns are separated
              into their own nodes and other text is preserved as-is.
    """
    new_nodes = []

    for old_node in old_nodes:
        # Only process plain text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        patterns = extractor_func(original_text)

        # If no patterns are found, keep the node unchanged
        if not patterns:
            new_nodes.append(old_node)
            continue

        # Iterate through all matched patterns in the text
        for content_text, url in patterns:
            # Determine the full markdown syntax to split on
            prefix = "!" if node_type == TextType.IMAGE else ""
            pattern_markdown = f"{prefix}[{content_text}]({url})"
            sections = original_text.split(pattern_markdown, 1)

            # Ensure the markdown syntax is correctly formed
            if len(sections) != 2:
                raise ValueError(
                    f"Invalid markdown: incomplete or malformed {
                        pattern_type} pattern: {pattern_markdown}"
                )

            # Add text before the matched pattern (if any)
            before_text = sections[0]
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            # Add the matched pattern as a separate node
            new_nodes.append(TextNode(content_text, node_type, url))

            # Continue processing the remaining text
            original_text = sections[1]

        # Add any text remaining after the last pattern
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]):
    """
    Splits text nodes containing markdown image syntax into separate nodes.

    Args:
        old_nodes (list): List of TextNode objects to process.

    Returns:
        list: List of TextNode objects with images extracted into individual nodes.
    """
    return split_nodes_by_markdown_pattern(
        old_nodes,
        "Image",
        extract_markdown_images,
        TextType.IMAGE
    )


def split_nodes_link(old_nodes: List[TextNode]):
    """
    Splits text nodes containing markdown link syntax into separate nodes.

    Args:
        old_nodes (list): List of TextNode objects to process.

    Returns:
        list: List of TextNode objects with links extracted into individual nodes.
    """
    return split_nodes_by_markdown_pattern(
        old_nodes,
        "Link",
        extract_markdown_links,
        TextType.LINK
    )
