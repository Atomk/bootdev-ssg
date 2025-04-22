class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        No tag: this is plain text inside of another HTML node
        No value: this is just a container for other elements (i.e. <ul>, <section>)
        No children: this is a container for just text (i.e. <p>, <soan>, <h1>)
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
            html_string += f' {key}="{val}"'
        return html_string

    def __repr__(self):
        return f"HTMLNode(\n\t{self.tag}\n\t{self.value}\n\t{self.children}\n\t{self.props}\n)"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
