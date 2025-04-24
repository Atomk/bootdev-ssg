import unittest
from textnode import TextNode, TextType
from markdown_parser import split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()
