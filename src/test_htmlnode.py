import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

        node = HTMLNode(tag="a", value="Boot.dev", props={"href":"https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Boot.dev")
        self.assertIsNone(node.children)
        self.assertIsNotNone(node.props)
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
