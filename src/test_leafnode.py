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
        self.assertEqual(node.children, None)
        self.assertIn("href", node.props)
        self.assertEqual(node.props["href"], "https://boot.dev")

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

        node = create_bootdev_link()
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Boot.dev</a>')

        # TODO test element with double quotes inside value
        # TODO Add more tests for different tag types.


if __name__ == "__main__":
    unittest.main()
