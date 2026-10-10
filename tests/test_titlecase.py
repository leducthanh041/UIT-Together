"""Heading casing respects localization, inline markup and research names."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from i18n import localize_html, title_case


class TitleCaseTests(unittest.TestCase):
    def test_small_words_and_boundary_words(self):
        self.assertEqual(title_case('a guide to research in the lab'),
                         'A Guide to Research in the Lab')
        self.assertEqual(title_case('from here to'), 'From Here To')
        self.assertEqual(title_case('learning through collaboration and data'),
                         'Learning through Collaboration and Data')

    def test_acronyms_hyphenation_and_mixed_case(self):
        self.assertEqual(title_case('AI and WSI with MMDetection and BibTeX'),
                         'AI and WSI with MMDetection and BibTeX')
        self.assertEqual(title_case('sparse-view CT reconstruction'),
                         'Sparse-View CT Reconstruction')

    def test_inline_markup_shares_heading_boundaries(self):
        result = localize_html(
            '<h2>learning <em>in the</em> lab</h2><h3><a href="#">from here</a> to</h3>',
            'en', {}, set(), '/')
        self.assertEqual(result,
            '<h2>Learning <em>in the</em> Lab</h2><h3><a href="#">From Here</a> To</h3>')

    def test_casing_happens_after_translation(self):
        self.assertEqual(localize_html('<h2>Research grows through collaboration.</h2>',
            'vi', {'Research grows through collaboration.': 'Nghiên cứu phát triển qua hợp tác.'},
            set(), '/'), '<h2>Nghiên Cứu Phát Triển qua Hợp Tác</h2>')

    def test_heading_periods_are_removed_after_translation(self):
        result = localize_html('<h2>seeing further.</h2><h3>learning <em>together.</em> </h3>'
                               '<h4>research updates<span>.</span></h4><p>Keep this period.</p>',
                               'en', {}, set(), '/')
        self.assertEqual(result, '<h2>Seeing Further</h2><h3>Learning <em>Together</em> </h3>'
                                 '<h4>Research Updates<span></span></h4><p>Keep this period.</p>')

    def test_periods_in_protected_names_code_and_ellipses_remain(self):
        source = ('<h3 translate="no">a paper title.</h3>'
                  '<div class="venue-heading"><h2>Journal name.</h2></div>'
                  '<h3 class="member-name">Dr.</h3>'
                  '<h2>run <code>command.</code></h2><h2>more research...</h2>')
        result = localize_html(source, 'en', {}, set(), '/')
        self.assertIn('<h3 translate="no">a paper title.</h3>', result)
        self.assertIn('<h2>Journal name.</h2>', result)
        self.assertIn('<h3 class="member-name">Dr.</h3>', result)
        self.assertIn('<h2>Run <code>command.</code></h2>', result)
        self.assertIn('<h2>More Research...</h2>', result)

    def test_protected_names_code_and_regular_prose(self):
        source = ('<h3 translate="no">a paper with mixed case</h3>'
                  '<div class="venue-heading"><h2>Journal of lowercase names</h2></div>'
                  '<article class="contact-card"><h2>Nguyen van An</h2></article>'
                  '<h3 class="member-name">Le van Binh</h3>'
                  '<h2>training <code>num_classes</code> in <span translate="no">mmdetection</span></h2>'
                  '<p>regular prose in the lab</p>')
        result = localize_html(source, 'en', {}, set(), '/')
        self.assertIn('<h3 translate="no">a paper with mixed case</h3>', result)
        self.assertIn('<h2>Journal of lowercase names</h2>', result)
        self.assertIn('<h2>Nguyen van An</h2>', result)
        self.assertIn('<h3 class="member-name">Le van Binh</h3>', result)
        self.assertIn('<h2>Training <code>num_classes</code> in <span translate="no">mmdetection</span></h2>', result)
        self.assertIn('<p>regular prose in the lab</p>', result)

    def test_paper_page_title_is_preserved(self):
        result = localize_html('<title>a paper and its original title</title>'
                               '<h1>a paper and its original title</h1><h2>brief description</h2>',
                               'en', {}, set(), '/papers/paper/example.html')
        self.assertIn('<title>a paper and its original title</title>', result)
        self.assertIn('<h1>a paper and its original title</h1>', result)
        self.assertIn('<h2>Brief Description</h2>', result)


if __name__ == '__main__':
    unittest.main()
