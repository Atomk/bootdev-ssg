import unittest
import filegeneration


class TestHeadingExtraction(unittest.TestCase):
    def none_found(self):
        md = """#aaa

#bbb # lll

## ccc
### ddd

#eee
"""
        self.assertRaises(ValueError, lambda: filegeneration.extract_title(md))


    def one_h1(self):
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


    def multiple_h1(self):
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

    def nested_h1(self):
        md = """#aaa
## # zzz
## ppp # yyy
# bbb # xxx
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