import unittest
from htmlnode import LeafNode


def create_bootdev_link():
    return LeafNode("a", "Boot.dev", {"href":"https://boot.dev"})

class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        self.assertRaises(TypeError, lambda: LeafNode())

        node = create_bootdev_link()
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Boot.dev")
        self.assertIsNone(node.children)
        self.assertIn("href", node.props)
        self.assertEqual(node.props["href"], "https://boot.dev")

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

        node = create_bootdev_link()
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Boot.dev</a>')

        node = LeafNode(None, "This is a text node.")
        self.assertEqual(node.to_html(), "This is a text node.")

        # TODO test element with double quotes inside value
        # TODO Add more tests for different tag types.
        # TODO if an attribute has a numerical value, it should still be sourrended by double quotes
        # TODO only certain tags are allowed
        # TODO tags and attributes must be lowercase letters only (no numbers, symbols)
        # TODO every element can use only certain attributes
        # TODO void elements (hr, br, image)


if __name__ == "__main__":
    unittest.main()
