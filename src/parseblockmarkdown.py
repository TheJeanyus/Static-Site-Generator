def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n")]
    blocks = [block for block in blocks if block != ""]
    return blocks