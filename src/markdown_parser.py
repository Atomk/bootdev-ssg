import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        # TODO allow multiple levels of nested inline text types (like italic text inside of bold text)
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Number of delimiters must be even")

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # At even indexes there's the text between nodes
                # If a string starts with a delimiter, the first element
                # in the parts list will be an empty string. The same concept
                # applies to a delimiter at the end of the string.
                # An empty string should not create a new node.
                if part != "":
                    new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                # At odd indexes there's the text contained between delimiters.
                # Delimiters must have text between them.
                if part == "":
                    raise Exception("Found two matching delimiters without text between them")
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text) -> list[tuple]:
    alt_part = r"\[(.*?)\]"
    url_part = r"\((.*?)\)"
    pattern = "!" + alt_part + url_part
    return re.findall(pattern, text)


def extract_markdown_links(text) -> list[tuple]:
    # a link cannot be preceded by an exclamation mark
    negative_lookbehind = "(?<!!)"
    text_part = r"\[(.*?)\]"
    url_part = r"\((.*?)\)"
    pattern = negative_lookbehind + text_part + url_part
    return re.findall(pattern, text)
