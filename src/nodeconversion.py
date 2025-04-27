from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from markdown_parser import (
    text_to_textnodes,
)
from mdblock import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.NORMAL: return LeafNode(None, text_node.text)
        case TextType.BOLD: return LeafNode("b", text_node.text)
        case TextType.ITALIC: return LeafNode("i", text_node.text)
        case TextType.CODE: return LeafNode("code", text_node.text)
        case TextType.LINK: return LeafNode("a", text_node.text, { "href":text_node.url })
        case TextType.IMAGE: return LeafNode("img", text_node.text, { "src":text_node.url, "alt":text_node.text })
        case _:
            raise ValueError("Unhandled text type: " + text_node.text_type)


def _markdown_block_to_html_nodes_list(block: str):
    text_nodes = text_to_textnodes(block)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes


def _block_paragraph_to_html_nodes(block: str):
    # paragraph lines should turn into a single line of text
    stripped_lines = map(lambda s: s.strip(), block.splitlines())
    joined_text = " ".join(stripped_lines)
    html_nodes = _markdown_block_to_html_nodes_list(joined_text)
    return ParentNode("p", html_nodes)


def _block_heading_to_html_nodes(block: str):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    stripped_block = block.lstrip("#").lstrip()
    html_nodes = _markdown_block_to_html_nodes_list(stripped_block)
    return ParentNode(f"h{count}", html_nodes)


def _block_code_to_html_nodes(block: str):
    stripped_block = block.strip("`")
    # first line should be removed
    # TODO last line should be removed too it it starts with ``` (check before stripping it)
    first_line, code_text = stripped_block.split("\n", 1)
    code_node = TextNode(code_text, TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(code_node)])


def _block_quote_to_html_nodes(block: str):
    stripped_lines = []
    for line in block.splitlines():
        stripped_lines.append(line.lstrip().lstrip(">").lstrip())
    text = "\n".join(stripped_lines)
    html_nodes = _markdown_block_to_html_nodes_list(text)
    return ParentNode(f"blockquote", html_nodes)


def markdown_to_html_tree(markdown: str) -> ParentNode:
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH: nodes.append(_block_paragraph_to_html_nodes(block))
            case BlockType.HEADING: nodes.append(_block_heading_to_html_nodes(block))
            case BlockType.CODE: nodes.append(_block_code_to_html_nodes(block))
            case BlockType.QUOTE: nodes.append(_block_quote_to_html_nodes(block))
            case BlockType.UNORDERED_LIST: pass
            case BlockType.ORDERED_LIST: pass
            case _: raise ValueError(f"Unhandled block type: {block_type}")

    return ParentNode("div", nodes)
