import re
from textnode import TextNode, TextType
from typing import List, Tuple


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """Splits text nodes by a given delimiter and assigns a specified text type to delimited sections.

    This function processes a list of text nodes, identifying occurrences of a given delimiter within 
    text-type nodes. It splits the text into alternating normal and formatted segments, creating 
    new nodes accordingly. Any non-text nodes are preserved as-is.

    The function assumes well-formed input where each opening delimiter has a matching closing 
    delimiter. If an unmatched delimiter is detected, a ValueError is raised.

    Args:
        old_nodes (List[TextNode]): The input list of text nodes.
        delimiter (str): The character or sequence used to identify formatted sections.
        text_type (TextType): The text type assigned to the delimited sections.

    Returns:
        List[TextNode]: A new list of nodes with correctly split and formatted text segments.

    Raises:
        ValueError: If the input text contains unmatched delimiters.

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
        # If node is not plain text, keep it unchanged
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split text based on the delimeter
        sections = node.text.split(delimiter)

        # Ensures that every opening delimiter has a matching closing delimiter.
        # A well-formed delimited section should always have an odd number of segments.
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown: Unmatched delimiter found")

        # Iterate over each section in the split text along with its index
        for index, section in enumerate(sections):
            # Ignore empty sections (caused by consecutive delimiters)
            if section:
                if index % 2 == 0:
                    # Even index: This is normal text outside the delimiters
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    # Odd index: This is formatted text (inside delimiters)
                    new_nodes.append(TextNode(section, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extract all markdown image references from text.

    Args:
        text (str): The markdown text to search

    Returns:
        list of tuples: Each tuple contains (alt_text, image_url)

    Example:
        >>> text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        >>> extract_markdown_images(text)
        [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extract all markdown hyperlinks from text, excluding image references.

    Args:
        text (str): The markdown text to search

    Returns:
        list of tuples: Each tuple contains (anchor_text, link_url)

    Example:
        >>> text = "This is text with a link [to boot dev](https://www.boot.dev)"
        >>> extract_markdown_links(text)
        [('to boot dev', 'https://www.boot.dev')]
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
