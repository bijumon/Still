#!/usr/bin/env python

# Still.py shows help when no arguments are given
# Still.py source-folder output-folder
# Still.py test runs unittests
#
# A Page or Post has frontmatter
# A Page is processed as a Jinja2 template
# A post is processed as a markdown or djot document
# Pages and Posts are processed through a layout template 

from dataclasses import dataclass, asdict
from os import walk, getcwd
from os.path import expanduser, exists, join, realpath, relpath, splitext
from pathlib import Path
from pprint import pprint
from tomllib import loads as toml_load_from_str, load as toml_load_from_file

@dataclass
class Defaults:
    title: str = "Still static site generator"
    source_dir: Path = Path(getcwd())
    output_dir: Path = Path(getcwd())
    exclude: list = None
    extensions: list = None
    limit_posts: int = 9
    permalink: str = "date"

    def __post_init__(self):
        if self.exclude is None:
            self.exclude = ['env', 'venv']
        if self.extensions is None:
            self.extensions = ["md", "cmark", "dj", "djot", "j2", "jinja2"]

class Post:
    def __init__(self, content_file):
        self.content_file = content_file
        _content_file = ContentFile(self.content_file)
        _content_file.load()

        self.frontmatter = _content_file.frontmatter()
        self.content = _content_file.content()
    
    def __str__(self):
        return str(self.content_file)

class ContentFile:
    def __init__(self, file: Path) -> None:
        self.file = file
        self.metadata: dict = {}
        self.text: str = ""

    def load(self) -> bool:
        if self.has_frontmatter():
            with open(self.file, "r") as f:
                self.metadata, self.text = f.read().split("+++", 2)[1:]
            return True

    def has_frontmatter(self) -> bool:
        with open(self.file, "r") as f:
            first_line = f.readline().strip()
        if first_line == "+++":
            return True
    
    def generate(self):
        file_name, file_ext = splitext(self.file)
        output_filename = file_name + ".html"

    def type(self):
        if str(self.file).endswith(".jinja2"):
            return "template"
        elif splitext(self.file)[1][1:] in site.config.extensions:
            return "document"

class FrontMatter:
    def __init__(self, metadata) -> None:
        self.metadata = metadata
    
    def parse(self):
        from tomllib import loads as toml_load_from_str
        return toml_load_from_str(self.metadata)
        
class Content:
    def __init__(self, text) -> None:
        self.text = text

    def frontmatter(self):
        frontmatter = FrontMatter(self.metadata)
        return frontmatter.parse()
    
    def content(self):
        content = Content(self.text)
        return content.render(self.siteconfig, self.frontmatter())

    def old_render(self):
        from markdown_it import MarkdownIt
        commonmark = MarkdownIt('commonmark')
        return commonmark.render(self.text)
    
class Permalink:
    def __init__(self, format) -> None:
        pass

class Site:
    def __init__(self, source_dir, output_dir) -> None:
        self.source_dir = self.fullpath(source_dir)
        self.output_dir = join(self.fullpath(output_dir), '_site')
        self.config = self.merge_defaults()
    
    def merge_defaults(self):
        site_config = SiteConfig(self.source_dir).load()
        site_defaults = asdict(Defaults())
    
        merged = site_defaults.copy()  # Make a shallow copy of d
        for key, value in site_config.items():
            if key in merged:
                if isinstance(merged[key], list) and isinstance(value, list):
                    merged[key].extend(value)  # If both values are lists, extend them
                else:
                    merged[key] = value  # else overwrite with the value from s
            else:
                merged[key] = value  # If key is not present, add it to merged
        return merged

    def fullpath(self, path) -> str:
        if len(path) == 0:
            return getcwd()
        elif '~' in path:
            return realpath(expanduser(path))
        else:
            return realpath(path)

class SiteConfig:
    def __init__(self, source_dir: Path) -> None:
        self.source_dir = source_dir
        self.config: dict = {}

    def load(self):
        config_file = join(self.source_dir, "config.toml")
        if exists(config_file):
            with open(config_file, "rb") as f:
                self.config = toml_load_from_file(f)
        return self.config

class ContentList:
    def find(self) -> list:
        content_files = []

        for root, dirs, files in walk(expanduser(site.source_dir), topdown=True):
            dirs[:] = [d for d in dirs if not (d[0] == '.' or d[0] == '_')]
            files = [f for f in files if f.endswith(".md") or f.endswith('.jinja2')]
            for file in files:
                content_files.append(join(root, file))
        return content_files

if __name__ == '__main__':
    site = Site("test/sample", "site")
    pprint(site.config)
    site.content_list = ContentList().find()
    for cfile in site.content_list:
        content_file = ContentFile(cfile)
        content_file.load()

        if content_file.type() == "template":
            t = Template(content_file.metadata, content_file.text)
        elif content_file.type() == "document":
            c = Content(content_file.metadata, content_file.text)

        #content_file.generate()

