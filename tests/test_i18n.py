"""Check bilingual navigation, preserved code and verified contact information."""
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from i18n import localize_html

class LanguageTests(unittest.TestCase):
    def test_localization_preserves_code_and_identifiers(self):
        source = '<html lang="en"><p>Research</p><pre>Research &lt;x&gt;</pre><h3 translate="no">Research</h3></html>'
        result = localize_html(source, 'vi', {'Research':'Nghiên cứu'}, {'/'}, '/')
        self.assertIn('<html lang="vi">', result)
        self.assertIn('<p>Nghiên cứu</p>', result)
        self.assertIn('<pre>Research &lt;x&gt;</pre>', result)
        self.assertIn('<h3 translate="no">Research</h3>', result)

    def test_language_and_asset_links(self):
        source = '<a href="./guide.html">Read</a><a href="/tutorials/" data-language-link>EN</a><img src="./assets/logo.png"><a href="https://doi.org/10.1234/x">DOI</a>'
        result = localize_html(source, 'vi', {}, {'/tutorials/', '/tutorials/guide.html'}, '/tutorials/')
        self.assertIn('href="/vi/tutorials/guide.html"', result)
        self.assertIn('href="/tutorials/" data-language-link', result)
        self.assertIn('src="/assets/logo.png"', result)
        self.assertIn('href="https://doi.org/10.1234/x"', result)

    def test_generated_routes_and_contact(self):
        english = (ROOT/'dist/index.html').read_text()
        vietnamese = (ROOT/'dist/vi/index.html').read_text()
        self.assertIn('<html lang="en">', english)
        self.assertIn('<html lang="vi">', vietnamese)
        self.assertIn('href="/vi/papers/"', vietnamese)
        self.assertIn('href="/vi/" data-language-link', english)
        self.assertIn('lab-logo.svg', english)
        self.assertIn('lab-logo.svg', vietnamese)
        for language in ['', 'vi/']:
            contact = (ROOT/f'dist/{language}contact/index.html').read_text()
            self.assertIn('mailto:khanhnd@uit.edu.vn', contact)
            self.assertIn('Nguyen Tan Tran Minh Khang', contact)
            self.assertIn('Khanh Duy Nguyen', contact)
        self.assertIn('President · Associate Professor, PhD', (ROOT/'dist/contact/index.html').read_text())
        self.assertIn('Hiệu trưởng · Phó Giáo sư, Tiến sĩ', (ROOT/'dist/vi/contact/index.html').read_text())
        redirect = (ROOT/'dist/vi/homes/index.html').read_text()
        self.assertIn('content="0; url=/vi/"', redirect)

if __name__ == '__main__': unittest.main()
