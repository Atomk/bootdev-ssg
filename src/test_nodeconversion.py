import unittest
import nodeconversion
from textnode import TextNode, TextType

class TestNodeConversion(unittest.TestCase):
    def test_text_styles(self):
        input = TextNode("Hola", TextType.NORMAL)
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), "Hola")

        input = TextNode("Hola", TextType.BOLD)
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), "<b>Hola</b>")

        input = TextNode("Hola", TextType.ITALIC)
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), "<i>Hola</i>")

    def test_ignore_props(self):
        input = TextNode("Hola", TextType.NORMAL, "https://example.com")
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), "Hola")

        input = TextNode("Hola", TextType.BOLD, "https://example.com")
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), "<b>Hola</b>")

    def test_code(self):
        input = TextNode('print("hello")', TextType.CODE)
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), '<code>print("hello")</code>')

        input = TextNode('<p>test</p>', TextType.CODE)
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), '<code>&lt;p&gt;test&lt;/p&gt;</code>')

    def test_link(self):
        input = TextNode('Boot.dev', TextType.LINK, "https://boot.dev")
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), '<a href="https://boot.dev">Boot.dev</a>')

        # missing url
        input = TextNode('Boot.dev', TextType.LINK)
        output = nodeconversion.text_node_to_html_node(input)
        # TODO should raise error
        # self.assertRaises(ValueError, output.to_html)
        # TODO these tests are not strictly about conversion but more about valid node creation, should move to textnode tests
        # TODO missing text
        # TODO invalid URL

    def test_image(self):
        input = TextNode('This is alt text', TextType.IMAGE, "https://i.imgur.com/vclKmAP.jpeg")
        output = nodeconversion.text_node_to_html_node(input)
        self.assertEqual(output.to_html(), '<img src="https://i.imgur.com/vclKmAP.jpeg" alt="This is alt text" />')

        # TODO copy link tests
        # TODO src is mandatory != ""
        # TODO alt text is mandatory (not really but helps debug and accessibility)
        pass


if __name__ == "__main__":
    unittest.main()
