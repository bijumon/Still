#!/usr/bin/env python

from pathlib import Path
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
        self.assertDictEqual(
            result, {'name': 'python-Still', 'description': 'convert markdown to html'})

from Still import FrontMatter, ContentFile
class TestContentFile(unittest.TestCase):
    def test_load_pass(self):
        sample_pass_file = ContentFile("test/sample/blog_index.jinja2")
        if sample_pass_file.load():
            result = FrontMatter(sample_pass_file.metadata).parse()
        self.assertEqual(result["title"], "blog index")
    
    def test_load_fail(self):
        sample_fail_file = ContentFile("test/sample/default.jinja2")
        self.assertFalse(sample_fail_file.load())

class TestTemplate(unittest.TestCase):
    pass
