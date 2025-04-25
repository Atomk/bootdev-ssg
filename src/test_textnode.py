import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Italic text", TextType.ITALIC)
        self.assertEqual(str(node), "TextNode('Italic text', TextType.ITALIC, None)")
        image = TextNode("An image", TextType.IMAGE, "https://i.imgur.com/vclKmAP.jpeg")
        self.assertEqual(str(image), "TextNode('An image', TextType.IMAGE, 'https://i.imgur.com/vclKmAP.jpeg')")


if __name__ == "__main__":
    unittest.main()
