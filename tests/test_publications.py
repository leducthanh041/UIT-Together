"""Validate merged display data and the newly unified public routes."""
import json
import html
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import publication_groups

class PublicationDirectoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {p.stem: json.loads(p.read_text()) for p in (ROOT/'src/data').glob('*.json')}
        cls.groups = publication_groups(cls.data)

    def test_every_source_record_survives_merge(self):
        rows = [row for group in self.groups for row in group['publications']]
        ids = [key for row in rows for key in row['source_ids']]
        self.assertCountEqual(ids, self.data['publications'].keys())
        for row in rows:
            for key in row['source_ids']:
                self.assertIn(self.data['publications'][key]['citation'], row['citations'])

    def test_venue_groups_have_consistent_filter_metadata(self):
        for group in self.groups:
            for row in group['publications']:
                self.assertEqual(group['venue']['name'], row['venue_name'])
                self.assertEqual(group['venue']['type'], row['publication_type'])
                self.assertTrue(row['display_title'])
                self.assertIn(row['publication_type'], ['journal', 'conference', 'unknown'])

    def test_years_are_not_merged_and_conflicting_dois_are_not_hidden(self):
        for group in self.groups:
            for row in group['publications']:
                records = [self.data['publications'][key] for key in row['source_ids']]
                self.assertEqual(len({record['year'] for record in records}), 1)
                dois = {record['doi'].casefold() for record in records if record['doi']}
                self.assertLessEqual(len(dois), 1)

    def test_alias_and_contact_are_published(self):
        alias = (ROOT/'dist/PapersByYear/index.html').read_text()
        self.assertIn('http-equiv="refresh" content="0; url=/papers/"', alias)
        papers = (ROOT/'dist/papers/index.html').read_text()
        for marker in ['data-year-filter', 'data-type-filter', 'data-venue-filter', 'data-venue-group']:
            self.assertIn(marker, papers)
        contact = (ROOT/'dist/contact/index.html').read_text()
        self.assertIn('mailto:khangnttm@uit.edu.vn', contact)
        self.assertIn('Nguyen Tan Tran Minh Khang', contact)
        self.assertIn('Khanh Duy Nguyen', contact)
        self.assertNotIn('Thầy', contact)
        home_alias = (ROOT/'dist/homes/index.html').read_text()
        self.assertIn('http-equiv="refresh" content="0; url=/"', home_alias)
        home = (ROOT/'dist/index.html').read_text()
        self.assertIn('class="home-wordmark"', home)
        self.assertIn('Computer Vision', home)
        self.assertIn('Machine Learning', home)
        self.assertEqual([item['url'] for item in self.data['site']['nav']].count('/'), 1)
        self.assertNotIn('/homes/', [item['url'] for item in self.data['site']['nav']])

    def test_verified_dois_have_clickable_links(self):
        papers = (ROOT/'dist/papers/index.html').read_text()
        for record in self.data['publications'].values():
            if record['doi']:
                self.assertRegex(record['doi'], r'^10\.\d{4,9}/\S+$')
                url = html.escape('https://doi.org/' + record['doi'], quote=True)
                self.assertIn('href="' + url + '"', papers)

if __name__ == '__main__':
    unittest.main()
