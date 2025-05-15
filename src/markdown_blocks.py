from enum import Enum
from typing import List
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Splits a Markdown document into block-level elements.

    A block is defined as text separated by one or more blank lines.
    Leading and trailing whitespace in each block is removed.
    Empty blocks (including those made up of only whitespace) are excluded.

    Args:
        markdown (str): The full Markdown string.

    Returns:
        List[str]: A list of cleaned, non-empty block strings.
    """
    # 1. Split the markdown text by double newlines.
    blocks = markdown.split("\n\n")

    # 2. Use a list comprehension to:
    #    a. Iterate through each potential block.
    #    b. Strip leading/trailing whitespace from the block.
    #    c. Keep the block *only if* it's not empty after stripping.

    cleaned_blocks = [block.strip() for block in blocks if block.strip()]

    return cleaned_blocks


def block_to_block_type(block: str) -> BlockType:
    """
    Determines the BlockType of a given markdown block.

    Args:
        block (str): A markdown block with leading/trailing whitespace stripped.

    Returns:
        BlockType: The identified type of the markdown block.
    """

    lines = block.split("\n")

    # # Heading: starts with 1-6 '#' characters followed by a space
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code block: starts and ends with a line containing triple backticks
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Quote block: every line must start with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list block: every line must start with '- ' (dash and space)
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST

    # Ordered list block: lines must be in the form '1. ', '2. ', ..., in order
    if lines[0].startswith("1. "):
        for expected_number, line in enumerate(lines, start=1):
            if not line.startswith(f"{expected_number}. "):
                break
        else:
            return BlockType.OLIST

    # Default case: paragraph
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Converts a full markdown document into a single parent HTMLNode.

    The parent HTMLNode (a 'div') contains child HTMLNode objects
    representing the nested markdown elements.

    Args:
        markdown: The markdown string to convert.

    Returns:
        A ParentNode ('div') containing the HTML representation of the markdown.
    """
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    """
    Converts a markdown block to its appropriate HTML node.

    Args:
        block (str): A markdown block string.

    Returns:
        ParentNode: The HTML node corresponding to the markdown block.

    Raises:
        ValueError: If the block type is invalid or unsupported.
    """
    block_type = block_to_block_type(block)

    # Use a dictionary to map block types to their respective handler functions
    block_handlers = {
        BlockType.PARAGRAPH: paragraph_to_html_node,
        BlockType.HEADING: heading_to_html_node,
        BlockType.CODE: code_to_html_node,
        BlockType.OLIST: olist_to_html_node,
        BlockType.ULIST: ulist_to_html_node,
        BlockType.QUOTE: quote_to_html_node
    }

    handler = block_handlers.get(block_type)
    if handler:
        return handler(block)

    raise ValueError(f"Unsupported block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
