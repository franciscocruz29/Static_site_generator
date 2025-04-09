from typing import List

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
