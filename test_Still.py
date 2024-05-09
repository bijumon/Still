#!/usr/bin/env python 

import unittest 

class TestPost(unittest.TestCase):

    def test_markdown(self):
        from markdown_it import MarkdownIt
        commonmark = MarkdownIt('commonmark')

        text = "**bold text**"
        result = commonmark.render(text)
        self.assertEqual(result, "<p><strong>bold text</strong></p>\n")

    def test_frontmatter(self):
        import tomllib

        data = """
            name = "python-Still"
            description = "convert markdown to html"
        """

        result = tomllib.loads(data)
        self.assertDictEqual(result, {'name': 'python-Still', 'description': 'convert markdown to html'})

class TestPage(unittest.TestCase):
    pass

class TestSite(unittest.TestCase):
    pass

