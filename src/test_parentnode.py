import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_constructor(self):
        self.assertRaises(TypeError, lambda: ParentNode())

    def test_empty_node(self):
        node = ParentNode("div", None)
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

        self.assertRaises(ValueError, node.to_html)

    def test_to_html(self):
        # no tag
        node = ParentNode(None, [])
        self.assertRaises(ValueError, node.to_html)

        # wrong container type
        node = ParentNode("div", "")
        self.assertRaises(ValueError, node.to_html)

        # no children
        node = ParentNode("div", [])
        self.assertEqual(
            node.to_html(),
            "<div></div>"
        )

        # no children, with attributes
        node = ParentNode("div", [], {"id": "main", "class": "center"})
        self.assertEqual(
            node.to_html(),
            '<div id="main" class="center"></div>'
        )

        # multiple children
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

        # multiple descendants
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [ LeafNode(None, "A paragraph!") ]
                ),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "First"),
                        LeafNode("li", "Second"),
                        LeafNode("li", "Third"),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>A paragraph!</p><ul><li>First</li><li>Second</li><li>Third</li></ul></div>"
        )


if __name__ == "__main__":
    unittest.main()