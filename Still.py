#!/usr/bin/env python

# Still.py shows help when no arguments are given
# Still.py source-folder publish-folder
# Still.py test runs unittests

from os import walk, getcwd
from os.path import expanduser, join, realpath, splitext
from pprint import pprint

class ContentList:
    def __init__(self, source_dir, publish_dir) -> None:
        self.exclude = set(['env', 'venv'])
        self.source_dir = source_dir
        self.publish_dir = publish_dir
        self.files = self.find()

    def find(self):
        content_files = []

        for root, dirs, files in walk(expanduser(self.source_dir), topdown=True):
            dirs[:] = [d for d in dirs if not (
                d in self.exclude or d[0] == '.' or d[0] == '_')]
            files = [f for f in files if f.endswith(".md")] 
                     #or f.endswith('.jinja') or f.endswith('.html')]
            for file in files:
                content_files.append(join(root, file))
        return content_files

class ContentFile:
    def __init__(self, content_file) -> None:
        self.content_file = content_file

    def load(self):
        with open(self.content_file, "r") as f:
            self.metadata, self.text = f.read().split("+++", 2)[1:]
    
    def frontmatter(self):
        _frontmatter = FrontMatter(self.metadata)
        return _frontmatter.parse()
    
    def content(self):
        _content = Content(self.text)
        return _content.render()

class FrontMatter:
    def __init__(self, metadata) -> None:
        self.metadata = metadata
    
    def parse(self):
        from tomllib import loads as toml_load_from_str
        return toml_load_from_str(self.metadata)
        
class Content:
    def __init__(self, text) -> None:
        self.text = text

    def render(self):
        from markdown_it import MarkdownIt
        commonmark = MarkdownIt('commonmark')
        return commonmark.render(self.text)

class Post:
    def __init__(self, content_file):
        self.content_file = content_file
        _content_file = ContentFile(self.content_file)
        _content_file.load()

        self.frontmatter = _content_file.frontmatter()
        self.content = _content_file.content()
    
    def __str__(self):
        return str(self.content_file)

class Site:
    def __init__(self, source_dir, publish_dir) -> None:
        self.source_dir = self.fullpath(source_dir)
        self.publish_dir = join(self.fullpath(publish_dir), '_site')

    def fullpath(self, path) -> str:
        if len(path) == 0:
            return getcwd()
        elif '~' in path:
            return realpath(expanduser(path))
        else:
            return realpath(path)
    
    def generate(self):
        _clist = ContentList(self.source_dir, self.publish_dir)
        for _clistfile in _clist.files:
            print(_clistfile)
            post = Post(_clistfile)
            file_name, file_ext = splitext(_clistfile)
            publish_file = file_name + ".html"
            with open(publish_file, "w") as f:
                f.write(post.content)

if __name__ == '__main__':
    s = Site("test/sample","")
    s.generate()
