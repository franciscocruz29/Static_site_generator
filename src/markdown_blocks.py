from enum import Enum
from typing import List


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

    Assumes leading/trailing whitespace is already stripped.
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
