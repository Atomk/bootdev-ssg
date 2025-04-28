import unittest
import filegeneration


class TestHeadingExtraction(unittest.TestCase):
    def test_none_found(self):
        md = """#aaa

#bbb # lll

## ccc
### ddd

#eee
"""
        self.assertRaises(ValueError, lambda: filegeneration.extract_title(md))


    def test_one_h1(self):
        md = """#aaa

# bbb

## ccc
### ddd

# eee
"""
        self.assertEqual(
            "bbb",
            filegeneration.extract_title(md)
        )


    def test_multiple_h1(self):
        md = """#aaa
#ddd
# bbb
# ccc
# ddd
# eee
"""
        self.assertEqual(
            "bbb",
            filegeneration.extract_title(md)
        )

    def test_nested_h1(self):
        md = """#aaa
## # zzz
## ppp # yyy
## ccc
### ddd
# eee
"""
        self.assertEqual(
            "eee",
            filegeneration.extract_title(md)
        )


if __name__ == "__main__":
    unittest.main()