import unittest
from mdblock import (
    markdown_to_blocks,
    is_heading,
    is_ordered_list,
    block_to_block_type,
    BlockType,
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


    def test_is_unordered_list(self):
        self.assertEqual(block_to_block_type("- one\n- two\n- three"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- one - one\n- two - two\n- three - three - three"), BlockType.UNORDERED_LIST)
        # space is allowed before list items
        self.assertEqual(block_to_block_type("- one\n-    two\n        - three"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("    - one     \n  - two\n    - three    "), BlockType.UNORDERED_LIST)

        # line starting with multiple item decorators
        self.assertNotEqual(block_to_block_type("-- one"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- one\n-- two\n- three"), BlockType.UNORDERED_LIST)
        # line not starting with item decorator
        self.assertNotEqual(block_to_block_type("one - one"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("one - one\ntwo - two\n- three"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- one\n- two\nthree - three"), BlockType.UNORDERED_LIST)
        # missing space between separator and text
        self.assertNotEqual(block_to_block_type("-one\n- two\n- three"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- one\n- two\n-three"), BlockType.UNORDERED_LIST)
        # mixed item decorator type
        self.assertNotEqual(block_to_block_type("* one\n- two\n- three"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- one\n- two\n* three"), BlockType.UNORDERED_LIST)


    def test_block_type(self):
        # NOTE headings and lists are already tested above
        self.assertEqual(block_to_block_type("one 1. one\ntwo 2. two\n3. three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("one - one\n- two\n- three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-one\n- two\n- three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- one\n- two\n-three"), BlockType.PARAGRAPH)

        # QUOTES
        self.assertEqual(block_to_block_type("> one\n> two\n> three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">one\n>two\n>three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">one\n> two\n> three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> one\n> two\n>three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> one\n  > two\n   >three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">one\n  >    two\n   >      three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("    >   one\n >   two\n>three"), BlockType.QUOTE)
        # repeated quote symbol
        self.assertEqual(block_to_block_type(">> one\n> two\n> three"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> one\n> two\n>> three"), BlockType.QUOTE)
        # not quotes
        self.assertEqual(block_to_block_type("< one\n> two\n> three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> one\n> two\n< three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> one\n> two\nthree"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> one\ntwo\n> three"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("* one\ntwo\n> three"), BlockType.PARAGRAPH)

    def test_is_code_block(self):
        self.assertEqual(block_to_block_type("```one\ntwo\nthree```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\none\ntwo\nthree```"), BlockType.CODE)
        # TODO this may be disallowed by the block splitting logic
        self.assertEqual(block_to_block_type("```\none\n\n\n\ntwo\nthree```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\none\n```\nthree\n```"), BlockType.CODE)
        # not code
        # space is not allowed before the code block
        self.assertEqual(block_to_block_type("    ```\none\ntwo\nthree\n```  "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("no    ```\none\ntwo\nthree\n```"), BlockType.PARAGRAPH)
        # TODO these should be impossible to get because the blocks parser strips whitespace
        self.assertEqual(block_to_block_type("```\none\ntwo\nthree```     "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\none\ntwo\nthree\n```     "), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()