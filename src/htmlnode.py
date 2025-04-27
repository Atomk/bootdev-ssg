def escape_html(html: str):
    CONVERSION_TABLE = (
        ("&", "&amp;"),
        (">", "&gt;"),
        ("<", "&lt;"),
    )

    escaped = html
    for pair in CONVERSION_TABLE:
        escaped = escaped.replace(pair[0], pair[1])
    return escaped


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        No tag: this is plain text inside of another HTML node
        No value: this is just a container for other elements (i.e. `<ul>`, `<section>`)
        No children: this is a container for just text (i.e. `<p>`, `<soan>`, `<h1>`)
        No props: the element has no attributes
        """

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        html_string = ""
        for key, val in self.props.items():
            # HTML attributes must be separated by spaces
            # TODO what if the value contains double quotes?
            html_string += f' {key}="{val}"'
        return html_string

    def __repr__(self):
        return f"HTMLNode(\n\t{self.tag}\n\t{self.value}\n\t{self.children}\n\t{self.props}\n)"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            if self.value is None or self.value == "":
                raise ValueError(f"A plain text node must have a value")
            return self.value
        if self.tag in ("img", "br", "hr"):
            return f"<{self.tag}{self.props_to_html()} />"
        if self.value is None or self.value == "":
            raise ValueError(f"Node with tag {self.tag} must have a value")
        if self.tag == "code":
            return f"<{self.tag}{self.props_to_html()}>{escape_html(self.value)}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("A parent node must have a tag")
        if not isinstance(self.children, list):
            raise ValueError("`children` must be a list")
        # if len(self.children) == 0:
        #     raise ValueError("A parent node must have children")

        descendants_html = ""
        for child in self.children:
            descendants_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{descendants_html}</{self.tag}>"
