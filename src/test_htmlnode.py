import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

        node = HTMLNode("a", "Boot.dev", None, {"href":"https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Boot.dev")
        self.assertEqual(node.children, None)
        self.assertIn("href", node.props)
        self.assertEqual(node.props["href"], "https://boot.dev")

    def test_unimplemented(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_repr(self):
        node = HTMLNode()
        string = str(node)
        self.assertEqual(string, "HTMLNode(\n\tNone\n\tNone\n\tNone\n\tNone\n)")

        # TODO test a more complex object

    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

        # TODO test a more complex object


if __name__ == "__main__":
    unittest.main()
