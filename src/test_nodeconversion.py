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


class TestBlockNodeConversion(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_quote(self):
        expected = "<div><blockquote>This is <b>bolded</b> text and <i>italic</i> text\nin a <code>blockquote</code> tag.</blockquote></div>"

        md = """
>This is **bolded** text and _italic_ text
>in a `blockquote` tag.
"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(html, expected)

        # ignore space after delimiters
        md = """
> This is **bolded** text and _italic_ text
>    in a `blockquote` tag.
"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(html, expected)

        # ignore space before delimiters
        md = """
> This is **bolded** text and _italic_ text
   >   in a `blockquote` tag.
"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(html, expected)


    def test_headings(self):
        md = """#111

# 111

## 222

### 333

#### 444

##### 555

###### 666

####### 777
"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>#111</p><h1>111</h1><h2>222</h2><h3>333</h3><h4>444</h4><h5>555</h5><h6>666</h6><p>####### 777</p></div>",
        )


    def test_list_unordered(self):
        md = """ # Title

- one
-   two
-  three
"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )


    def test_list_ordered(self):
        md = """ # Title

1. one
0.   two
5.  three
"""
        node = nodeconversion.markdown_to_html_tree(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )




if __name__ == "__main__":
    unittest.main()
