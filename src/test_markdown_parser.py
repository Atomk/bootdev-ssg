import unittest
from textnode import TextNode, TextType
from markdown_parser import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestMarkdownParser(unittest.TestCase):
    def test_single_match(self):
        # bold
        old_node = TextNode("This is text with a **bolded phrase** in the middle", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

        # code
        old_node = TextNode("This is text with a `code block` inside", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" inside", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_matches(self):
        # two new nodes
        old_node = TextNode("Here's **one** and **two** bolded words.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Here's ", TextType.NORMAL),
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("two", TextType.BOLD),
            TextNode(" bolded words.", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_location(self):
        # new node at start
        old_node = TextNode("**node** at start", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("node", TextType.BOLD),
            TextNode(" at start", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

        # new node at end
        old_node = TextNode("node at **end**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("node at ", TextType.NORMAL),
            TextNode("end", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

        # new node at start and end
        old_node = TextNode("**start** and **end**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("start", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("end", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_content_between_delimiters(self):
        old_node = TextNode("empty node ****!", TextType.NORMAL)
        function = lambda: split_nodes_delimiter([old_node], "**", TextType.BOLD)
        self.assertRaises(Exception, function)

    def test_odd_deimiters_count(self):
        # only left delimiter
        old_node = TextNode("This is text with **one delimiter", TextType.NORMAL)
        function = lambda: split_nodes_delimiter([old_node], "**", TextType.BOLD)
        self.assertRaises(Exception, function)

        # two matching delimiters + one unmatched
        old_node = TextNode("**what should happen here****?", TextType.NORMAL)
        function = lambda: split_nodes_delimiter([old_node], "**", TextType.BOLD)
        self.assertRaises(Exception, function)

    def test_other(self):
        # empty string
        old_node = TextNode("", TextType.NORMAL)
        # TODO

        # multiple different delimiters
        old_node = TextNode("The element `<div>` is **block-level**.", TextType.NORMAL)
        # TODO

        # nested delimiters
        old_node = TextNode("Markdown **allows _nested_ delimiters**.", TextType.NORMAL)
        # TODO


class TestLinkExtraction(unittest.TestCase):
    def test_image(self):
        text = "Text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(result, expected)

        matches = extract_markdown_images("Text with !![image](https://example.com/favicon.png))...")
        self.assertListEqual([("image", "https://example.com/favicon.png")], matches)

    def test_link(self):
        text = "A link to a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_links(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(result, expected)

        text = "A ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https"
        result = extract_markdown_links(text)
        self.assertListEqual(result, [])

        # TODO URL with invalid characters (spaces in between)
        # text = "A ![rick roll](https:// imgur com aK gif)"
        # result = extract_markdown_links(text)
        # self.assertListEqual(result, [])

        # TODO
        # text = "[what[rick roll](https://i.imgur.com/aKaOqIh.gif)]"
        # result = extract_markdown_links(text)
        # self.assertListEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

        # TODO nested
        # text = "[[nested](xxx)](yyy)]"
        # result = extract_markdown_links(text)
        # self.assertListEqual(result, [("nested", "xxx")])

    def test_mixed(self):
        # should not match the link
        matches = extract_markdown_images(
            "Text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        # should not match the image
        matches = extract_markdown_links(
            "Text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)


class TestLinkSplitting(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

        # Image at string start and end
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

        # ignore link
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://imgur.com/)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and [link](https://imgur.com/)", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links(self):
        # empty string
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

        # No links
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

        # Link at string start and end
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

        # ignore image
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://imgur.com/)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://imgur.com/"),
            ],
            new_nodes,
        )

        # ignore image (reversed)
        node = TextNode(
            "[link](https://imgur.com/) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://imgur.com/"),
                TextNode(" and ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.NORMAL),
            ],
            new_nodes,
        )


class TestTextToNodes(unittest.TestCase):
    def test_basic(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

        # sequence of duplicated mixed blocks
        text = "_italic_**text**`code block`_italic_`code block`"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("italic", TextType.ITALIC),
                TextNode("text", TextType.BOLD),
                TextNode("code block", TextType.CODE),
                TextNode("italic", TextType.ITALIC),
                TextNode("code block", TextType.CODE),
            ]
        )


if __name__ == "__main__":
    unittest.main()
