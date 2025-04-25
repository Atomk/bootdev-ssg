from enum import Enum

TextType = Enum("TextType", ["NORMAL", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"])

class TextNode:
    """Represents the kinds of inline text available in both Markdows and HTML."""

    def __init__(self,
                 text: str,
                 text_type: TextType,
                 url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
	        and self.url == other.url
        )

    def __repr__(self):
        url = self.url if self.url is None else f"'{self.url}'"
        return f"TextNode('{self.text}', {self.text_type}, {url})"
