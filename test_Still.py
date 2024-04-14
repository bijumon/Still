#!/usr/bin/env python 

import unittest 

class TestPost(unittest.TestCase):
    
    def test_markdown(self):
        from markdown_it import MarkdownIt
        commonmark = MarkdownIt('commonmark')

        text = "**bold text**"
        result = commonmark.render(text)
        self.assertEqual(result, "<p><strong>bold text</strong></p>\n")
