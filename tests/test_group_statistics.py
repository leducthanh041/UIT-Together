import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import publication_groups
from group_statistics import group_statistics


class GroupStatisticsTests(unittest.TestCase):
    def test_current_public_directories(self):
        data = {p.stem: json.loads(p.read_text()) for p in (ROOT / 'src/data').glob('*.json')}
        data['publication_groups'] = publication_groups(data)
        result = group_statistics(data, (ROOT / 'src/partials/datasets-content.html').read_text())
        self.assertEqual(result, dict(participants=140, papers=105, venues=42, datasets=13))

    def test_home_uses_computed_statistics_without_conference_widget(self):
        data = {p.stem: json.loads(p.read_text()) for p in (ROOT / 'src/data').glob('*.json')}
        data['publication_groups'] = publication_groups(data)
        counts = group_statistics(data, (ROOT / 'src/partials/datasets-content.html').read_text())
        for language in ['', 'vi/']:
            html = (ROOT / f'dist/{language}index.html').read_text()
            self.assertNotIn('data-conference-app', html)
            self.assertNotIn('/js/conferences.js', html)
            for count in counts.values():
                self.assertIn(f'class="lab-stat-number" translate="no">{count}</p>', html)
            self.assertNotIn('class="home-impact"', html)
        css = (ROOT / 'src/assets/css/portfolio.css').read_text()
        self.assertNotIn('.site-menu li:last-child a', css)

    def test_duplicate_names_and_unclassified_venues(self):
        data = {'members': [{'name': '  Nguyen  Van A '}], 'cohorts': [{'names': ['nguyen van a', 'B']}], 'publication_groups': [{'venue': {'type': 'journal'}, 'publications': [1, 2]}, {'venue': {'type': 'unknown'}, 'publications': [3]}]}
        datasets = '<h4 class="media-heading">Dataset A<small>2026</small></h4><h4 class="media-heading">Dataset A<small>2027</small></h4>'
        self.assertEqual(group_statistics(data, datasets), dict(participants=2, papers=3, venues=1, datasets=1))

if __name__ == '__main__': unittest.main()
