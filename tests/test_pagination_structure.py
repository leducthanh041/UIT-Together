"""Pagination items must remain siblings, never hidden by another page item."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class PaginationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.items = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-page-item' in attrs:
            self.items += 1
            if any('data-page-item' in ancestor for _, ancestor in self.stack):
                self.errors.append('Nested pagination item')
            if not any('data-paginate' in ancestor for _, ancestor in self.stack):
                self.errors.append('Pagination item without pagination scope')
        if tag not in VOID:
            self.stack.append((tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


class PaginationStructureTests(unittest.TestCase):
    def test_all_built_pages_have_independent_pagination_items(self):
        paths = list((ROOT / 'dist').rglob('*.html'))
        self.assertTrue(paths, 'Build the site before running this test')
        for path in paths:
            with self.subTest(page=str(path.relative_to(ROOT / 'dist'))):
                parser = PaginationParser()
                parser.feed(path.read_text())
                self.assertEqual(parser.errors, [])

    def test_all_datasets_are_independent_items(self):
        parser = PaginationParser()
        parser.feed((ROOT / 'src/partials/datasets-content.html').read_text())
        self.assertEqual(parser.errors, [])
        self.assertEqual(parser.items, 13)
