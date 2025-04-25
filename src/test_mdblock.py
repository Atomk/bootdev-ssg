import unittest
from mdblock import (
    markdown_to_blocks,
    is_heading,
    is_ordered_list,
    block_to_block_type,
)


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        # multiple newlines, strip leading spaces
        md = """     \n   \n   \n   \n     This is **bolded** paragraph
\n    \n\n\nThis is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
\n\n\n     - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_is_heading(self):
        self.assertTrue( is_heading("# title"))
        self.assertTrue( is_heading("## title"))
        self.assertTrue( is_heading("### title"))
        self.assertTrue( is_heading("###### title"))
        self.assertTrue( is_heading("## title ###### title"))
        self.assertFalse(is_heading("#title"))
        self.assertFalse(is_heading("###title"))
        self.assertFalse(is_heading("######title"))
        # Heading must be at line start
        self.assertFalse(is_heading("text ## title"))
        # TODO in most renderers this counts as two blocks
        self.assertFalse(is_heading("text\n## title"))


    def test_is_ordered_list(self):
        self.assertTrue( is_ordered_list("1. one\n2. two\n3. three"))
        self.assertTrue( is_ordered_list("1. one 1. one\n2. two 2. two\n3. three 3. three 3. three"))
        self.assertTrue( is_ordered_list("3. three\n2. two 2. two\n1. one"))
        self.assertTrue( is_ordered_list("0. zero\n105. one.oh.five"))
        self.assertTrue( is_ordered_list("000. zerozerozero\n0105. oh-one.oh.five\n1. one"))
        # space is allowed before list items
        self.assertTrue( is_ordered_list("1. one\n  2. two\n        3. three"))
        self.assertTrue( is_ordered_list("    1. one     \n  2. two\n    3. three    "))

        # line not starting with number
        self.assertFalse(is_ordered_list("one 1. one\ntwo 2. two\n3. three"))
        self.assertFalse(is_ordered_list("1. one\n2. two\nthree 3. three"))
        # missing space between separator and text
        self.assertFalse(is_ordered_list("1.one\n2.two\n3. three"))
        self.assertFalse(is_ordered_list("1. one\n2.two\n3.three"))
        # incorrect separator
        self.assertFalse(is_ordered_list("1, one\n2.two\n3.three"))
        self.assertFalse(is_ordered_list("1. one\n2.two\n3,three"))
        # mixed numbering type
        self.assertFalse(is_ordered_list("a. one\nb.two\n3.three"))
        self.assertFalse(is_ordered_list("1. one\n2.two\nc.three"))


if __name__ == "__main__":
    unittest.main()