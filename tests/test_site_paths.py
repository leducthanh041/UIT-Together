import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from site_paths import normalize_base_path, site_url, prefix_html, prefix_css


class SitePathsTests(unittest.TestCase):
    def test_project_paths_external_links_and_anchors(self):
        html = '<a href="/vi/team/">VI</a><img src="/assets/a.png"><video poster="/assets/p.png"></video><a href="https://doi.org/x">DOI</a><a href="//example.org/x">CDN</a><a href="#members">Members</a>'
        output = prefix_html(html, '/UIT-Together')
        self.assertIn('href="/UIT-Together/vi/team/"', output)
        self.assertIn('src="/UIT-Together/assets/a.png"', output)
        self.assertIn('poster="/UIT-Together/assets/p.png"', output)
        self.assertIn('href="https://doi.org/x"', output)
        self.assertIn('href="//example.org/x"', output)
        self.assertIn('href="#members"', output)
        self.assertEqual(prefix_html(output, '/UIT-Together'), output)

    def test_redirects_css_and_root_build(self):
        html = '<meta http-equiv="refresh" content="0; url=/vi/"><link href="/">'
        self.assertIn('url=/UIT-Together/vi/', prefix_html(html, '/UIT-Together'))
        self.assertEqual(prefix_html(html, ''), html)
        self.assertEqual(prefix_css('url(/assets/font.woff)', '/UIT-Together'), 'url(/UIT-Together/assets/font.woff)')
        self.assertEqual(site_url('/research/?q=vision#ct', '/UIT-Together'), '/UIT-Together/research/?q=vision#ct')
        self.assertEqual(normalize_base_path('/'), '')
        self.assertEqual(normalize_base_path('/UIT-Together/'), '/UIT-Together')
        for bad in ['https://example.com', '/a/../b', '/a//b', '/a?query=1']:
            with self.assertRaises(ValueError): normalize_base_path(bad)

if __name__ == '__main__': unittest.main()
