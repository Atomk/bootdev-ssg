
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped_blocks_map = map(lambda s: s.strip(), blocks)
    return list(filter(lambda text: text != "", stripped_blocks_map))
