#!/usr/bin/env python

# Still.py shows help when no arguments are given
# Still.py source-folder output-folder
# Still.py test runs unittests
#
# A Page or Post has frontmatter
# A Page is processed as a Jinja2 template
# A post is procedded as a markdown or djot document

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

class ContentList:
    def __init__(self, source_dir, output_dir) -> None:
        self.source_dir = source_dir
        self.output_dir = output_dir

    def find(self) -> list:
        content_files = []

        for root, dirs, files in walk(expanduser(self.source_dir), topdown=True):
            dirs[:] = [d for d in dirs if not (d[0] == '.' or d[0] == '_')]
            files = [f for f in files if f.endswith(".md") or f.endswith('.jinja2')]
            for file in files:
                content_files.append(join(root, file))
        return content_files

class ContentFile:
    def __init__(self, siteconfig: dict, content_file: Path) -> None:
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
    
    def generate(self):
        file_name, file_ext = splitext(self.content_file)
        output_file = file_name + ".html"
        print(f"{relpath(self.content_file)} -> {relpath(output_file)}")
        #with open(output_file, "w") as f:
        #    f.write(post.content)

class FrontMatter:
    def __init__(self, metadata) -> None:
        self.metadata = metadata
    
    def parse(self):
        from tomllib import loads as toml_load_from_str
        return toml_load_from_str(self.metadata)
        
class Content:
    def __init__(self, text) -> None:
        self.text = text

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
                    merged[key] = value  # Otherwise, overwrite with the value from s
            else:
                merged[key] = value  # If key is not present in d, add it to merged
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

if __name__ == '__main__':
    site = Site("test/sample", "site")
    content_list = ContentList(site.source_dir, site.output_dir)
    for _cfile in content_list.find():
        content_file = ContentFile(site.config, _cfile)
        content_file.generate()

