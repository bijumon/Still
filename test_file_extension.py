#!/usr/bin/env python

import unittest

class DocumentRenderer:
    def __init__(self, file_path):
        self.file_path = file_path

    def render(self):
        raise NotImplementedError("Subclasses must implement this method")

class PDFRenderer(DocumentRenderer):
    def render(self):
        # Logic to render PDF files
        return f"Rendering PDF document: {self.file_path}"

class WordRenderer(DocumentRenderer):
    def render(self):
        # Logic to render Word files
        return f"Rendering Word document: {self.file_path}"

class TextRenderer(DocumentRenderer):
    def render(self):
        # Logic to render text files
        return f"Rendering text document: {self.file_path}"

# Example usage:
file_path = "example.pdf"
if file_path.endswith('.pdf'):
    renderer = PDFRenderer(file_path)
elif file_path.endswith('.docx'):
    renderer = WordRenderer(file_path)
elif file_path.endswith('.txt'):
    renderer = TextRenderer(file_path)
else:
    print("Unsupported file format")


print(renderer.render())
