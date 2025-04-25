import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    stripped_blocks_map = map(lambda s: s.strip(), blocks)
    return list(filter(lambda text: text != "", stripped_blocks_map))


def is_heading(block: str) -> bool:
    return len(re.findall(r"^#{1,6} ", block)) > 0


def _every_line_starts_with(text: str, prefix: str) -> bool:
    lines = text.splitlines()
    for line in lines:
        if not line.strip().startswith(prefix):
            return False
    return True


def is_ordered_list(block: str):
    lines = block.splitlines()
    for line in lines:
        # Technically each number should increment by one,
        # but HTML numbers element automatically so we don't care
        matches = re.findall(r"^\d+\. ", line.strip())
        if len(matches) == 0:
            return False
    return True


def block_to_block_type(block: str) -> BlockType:
    if is_heading(block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif _every_line_starts_with(block, ">"):
        return BlockType.QUOTE
    elif _every_line_starts_with(block, "- "):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
