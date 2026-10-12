"""Home selections must use reviewed dates and preserve publication metadata."""
from copy import deepcopy
from datetime import date
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from home_content import home_context, reviewed_news, selected_publications


class HomeContentTests(unittest.TestCase):
    def setUp(self):
        self.data = {path.stem: json.loads(path.read_text()) for path in (ROOT / 'src/data').glob('*.json')}

    def test_new_reviewed_announcement_updates_top_three_without_template_changes(self):
        added = dict(self.data['news'][0], id='test-new-announcement', date='2026-10-01')
        self.data['news'].append(added)
        self.data['news'].reverse()
        context = home_context(self.data, today=date(2026, 10, 12))
        self.assertEqual([item['id'] for item in context['latest_news']], ['test-new-announcement', 'news-001', 'news-002'])
        self.assertFalse(context['news_is_historical'])

    def test_original_dates_and_unreviewed_records(self):
        context = home_context(self.data, today=date(2026, 10, 12))
        self.assertTrue(context['news_is_historical'])
        self.assertEqual(context['latest_news'][0]['date'], '2022-06-15')
        self.data['news'][0]['verified'] = False
        self.assertNotIn('news-001', [item['id'] for item in reviewed_news(self.data['news'])])

    def test_invalid_or_missing_dates_fail_instead_of_inventing_dates(self):
        for value in ['', '2026-02-30', '2026-1-1', 'Jan 2026']:
            with self.subTest(value=value):
                records = deepcopy(self.data['news'])
                records[0]['date'] = value
                with self.assertRaises(ValueError): reviewed_news(records)

    def test_missing_provenance_and_duplicate_ids_fail(self):
        records = deepcopy(self.data['news'])
        records[0]['date_source'] = ''
        with self.assertRaises(ValueError): reviewed_news(records)
        with self.assertRaises(ValueError): reviewed_news(self.data['news'] * 2)

    def test_highlights_preserve_source_and_explicit_order(self):
        before = deepcopy(self.data['publications'])
        identifiers = self.data['selected_achievements']
        selected = selected_publications(identifiers, self.data['publications'])
        self.assertEqual([item['id'] for item in selected], identifiers)
        self.assertEqual(self.data['publications'], before)
        for item in selected:
            self.assertTrue(item['authors'])
            self.assertEqual(item['publication_type'], 'journal')

    def test_invalid_highlight_selections_fail(self):
        for identifiers in [[], ['missing', 'also-missing'], ['954004f82493'] * 2, ['8bb6cc1ec45d', '09c496da2c87'], list(self.data['publications'])[:4]]:
            with self.subTest(identifiers=identifiers):
                with self.assertRaises(ValueError): selected_publications(identifiers, self.data['publications'])

    def test_home_and_news_render_only_group_content(self):
        for prefix in ['', 'vi/']:
            home = (ROOT / f'dist/{prefix}index.html').read_text()
            news = (ROOT / f'dist/{prefix}news/index.html').read_text()
            self.assertEqual(home.count('data-news-id='), 3)
            self.assertEqual(home.count('data-publication-id='), 3)
            self.assertEqual(home.count('<section '), 4)
            self.assertNotIn('data-paginate', home)
            self.assertNotIn('home-impact', home)
            self.assertIn('class="lab-statistics"', home)
            self.assertNotIn('View all news', home)
            self.assertNotIn('Xem tất cả tin tức', home)
            self.assertNotIn('Q1', home)
            self.assertEqual(news.count('data-news-id='), len(self.data['news']))
            self.assertNotIn('Kyle receives tenure', news)
            self.assertIn('2022-06-15', home)
            self.assertIn(f'href="/{prefix}news/#news-001"', home)
            for item in home_context(self.data)['research_highlights']:
                self.assertIn(item['authors'], home)
            self.assertTrue((ROOT / f'dist/{prefix}news/tenure-emily.html').exists())


if __name__ == '__main__':
    unittest.main()
