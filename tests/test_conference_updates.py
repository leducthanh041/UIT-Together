import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

spec = importlib.util.spec_from_file_location('conference_updater', Path(__file__).resolve().parents[1] / 'scripts/update_conferences.py')
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


def record(**changes):
    data = {'id': 'cvpr', 'acronym': 'CVPR', 'year': 2027, 'name': 'CVPR', 'topics': ['vision'], 'website': 'https://cvpr.thecvf.com/Conferences/2027', 'source_urls': [], 'starts_on': None, 'ends_on': None, 'deadlines': [], 'date_status': 'unannounced', 'location': '', 'last_success_at': None}
    data.update(changes)
    return data


class ConferenceUpdatesTests(unittest.TestCase):
    def test_dates_table_aoe_has_no_invented_clock(self):
        html = '<h1>CVPR 2027</h1><h3>Paper Submissions</h3><table><tr><td>Submission Deadline</td><td>Nov 16 \'26 (Anywhere on Earth)</td></tr></table>'
        parsed, _ = updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027/Dates')
        self.assertEqual(parsed['deadlines'][0]['date'], '2026-11-16')
        self.assertEqual(parsed['deadlines'][0]['zone'], 'AoE')
        self.assertIsNone(parsed['deadlines'][0]['at'])

    def test_explicit_clock_offset_and_date_only_without_zone(self):
        self.assertEqual(updater.explicit_time('23:59 UTC-12', updater.date(2026, 7, 28)), '2026-07-28T23:59:00-12:00')
        self.assertEqual(updater.explicit_time('11:59 PM AoE', updater.date(2026, 7, 28)), '2026-07-28T23:59:00-12:00')
        self.assertIsNone(updater.explicit_time('23:59', updater.date(2026, 7, 28)))

    def test_deleted_old_deadline_and_tentative_cue(self):
        html = '<h1>CVPR 2027</h1><h3>Proposed Paper Deadlines</h3><p>Full Paper Submission: <del>August 16, 2026</del> August 30, 2026 at 23:59 AoE</p>'
        parsed, _ = updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027')
        self.assertEqual(len(parsed['deadlines']), 1)
        self.assertEqual(parsed['deadlines'][0]['date'], '2026-08-30')
        self.assertEqual(parsed['deadlines'][0]['status'], 'tentative')

    def test_wrong_edition_and_navigation_year_rejected(self):
        html = '<h1>CVPR 2026</h1><nav>2027 2028</nav><p>Full Paper Submission: November 16, 2026</p>'
        with self.assertRaises(ValueError):
            updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027')

    def test_workshop_abstract_and_ambiguous_dates_are_not_main_paper(self):
        html = '<h1>CVPR 2027</h1><h3>Workshops</h3><p>Full Paper Submission: November 16, 2026</p><h3>Main Papers</h3><p>Abstract deadline: November 10, 2026</p><p>Full Paper Submission: November 16, 2026 or November 18, 2026</p>'
        self.assertEqual(updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027')[0]['deadlines'], [])

    def test_jsonld_event_dates_and_location(self):
        event = {'@context': 'https://schema.org', '@type': 'Event', 'name': 'CVPR 2027', 'startDate': '2027-06-22', 'endDate': '2027-06-25', 'location': {'name': 'Nashville'}}
        html = '<script type="application/ld+json">' + json.dumps({'@graph': [event]}) + '</script>'
        parsed, _ = updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027')
        self.assertEqual(parsed['ends_on'], '2027-06-25')
        self.assertEqual(parsed['location'], 'Nashville')

    def test_network_failure_preserves_last_good_dates_and_marks_stale(self):
        old = record(starts_on='2027-06-22', ends_on='2027-06-25', last_success_at='2026-10-01T00:00:00+00:00', deadlines=[{'label': 'Main Paper', 'date': '2026-11-16'}])
        result, errors = updater.refresh_record(old, datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=OSError('offline')))
        self.assertEqual(result['ends_on'], old['ends_on'])
        self.assertEqual(result['deadlines'], old['deadlines'])
        self.assertEqual(result['sync_status'], 'stale')
        self.assertTrue(errors)

    def test_rollover_clears_old_year_dates_location_and_deadlines_offline(self):
        old = record(year=2026, starts_on='2026-06-20', ends_on='2026-06-25', location='Old city', deadlines=[{'date': '2025-11-15'}])
        result, _ = updater.refresh_record(old, datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=OSError('offline')))
        self.assertEqual(result['year'], 2027)
        self.assertIsNone(result['ends_on'])
        self.assertEqual(result['deadlines'], [])
        self.assertEqual(result['location'], '')
        self.assertEqual(result['sync_status'], 'pending')

    def test_conflicting_official_dates_are_hidden(self):
        htmls = ['<h1>CVPR 2027</h1><p>Main Conference Sessions: June 22-25, 2027</p>', '<h1>CVPR 2027</h1><p>Main Conference Sessions: June 19-23, 2027</p>']
        result, _ = updater.refresh_record(record(), datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=htmls))
        self.assertIsNone(result['starts_on'])
        self.assertIsNone(result['ends_on'])
        self.assertEqual(result['sync_status'], 'conflicting')

    def test_contained_main_and_full_conference_spans_are_not_conflicting(self):
        htmls = ['<h1>CVPR 2027</h1><p>Main Conference Sessions: June 22-25, 2027</p>', '<h1>CVPR 2027</h1><p>Conference Dates: June 20-25, 2027</p>']
        result, _ = updater.refresh_record(record(), datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=htmls))
        self.assertEqual(result['starts_on'], '2027-06-20')
        self.assertNotEqual(result['sync_status'], 'conflicting')

    def test_iccv_rollover_obeys_biennial_cadence(self):
        old = record(id='iccv', acronym='ICCV', year=2025, ends_on='2025-10-25')
        result, _ = updater.refresh_record(old, datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=OSError('offline')))
        self.assertEqual(result['year'], 2027)

    def test_conflicting_deadlines_are_not_counted_down(self):
        htmls = ['<h1>CVPR 2027</h1><p>Full Paper Submission: November 16, 2026 AoE</p>', '<h1>CVPR 2027</h1><p>Full Paper Submission: November 18, 2026 AoE</p>']
        result, _ = updater.refresh_record(record(), datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=htmls))
        self.assertEqual(result['deadlines'], [])
        self.assertEqual(result['sync_status'], 'conflicting')

    def test_year_outside_edition_window_is_ignored(self):
        html = '<h1>CVPR 2027</h1><p>Full Paper Submission: November 16, 2024</p>'
        self.assertEqual(updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027')[0]['deadlines'], [])

    def test_cross_month_event_range_is_not_truncated(self):
        for text in ['Conference Dates: September 26–October 1, 2027', 'Conference Dates: 26 September–1 October 2027']:
            parsed, _ = updater.parse_page('<h1>CVPR 2027</h1><p>' + text + '</p>', record(), 'https://cvpr.thecvf.com/Conferences/2027')
            self.assertEqual(parsed['starts_on'], '2027-09-26')
            self.assertEqual(parsed['ends_on'], '2027-10-01')

    def test_wacv_rounds_use_heading_context(self):
        html = '<h1>CVPR 2027</h1><h3>Round 1 Paper Submissions</h3><p>Full Paper Submission: June 26, 2026</p><h3>Round 2 Paper Submissions</h3><p>Full Paper Submission: August 28, 2026</p>'
        parsed, _ = updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027')
        self.assertEqual([d['label'] for d in parsed['deadlines']], ['Main Paper (Round 1)', 'Main Paper (Round 2)'])

    def test_location_explicit_labels_only_not_footer_contact_or_tba(self):
        html = '<h1>CVPR 2027</h1><p>Location: Seattle, Washington, USA</p><footer><p>Location: Wrong footer address</p></footer><div class="contact"><p>Venue: Contact office</p></div><p>Conference Venue: TBA</p>'
        parsed, _ = updater.parse_page(html, record(), 'https://cvpr.thecvf.com/Conferences/2027')
        self.assertEqual(parsed['location'], 'Seattle, Washington, USA')
        rejected, _ = updater.parse_page('<h1>CVPR 2027</h1><h3>Contact Us</h3><p>Location: Office address</p>', record(), 'https://cvpr.thecvf.com/Conferences/2027')
        self.assertNotIn('location', rejected)
        for text in ['Conference Venue: To be announced', 'Welcome to Seattle!', 'Venue: Contact office']:
            parsed, _ = updater.parse_page('<h1>CVPR 2027</h1><p>' + text + '</p>', record(), 'https://cvpr.thecvf.com/Conferences/2027')
            self.assertNotIn('location', parsed)

    def test_new_edition_uses_explicit_new_location_dates_and_deadlines(self):
        old = record(year=2026, ends_on='2026-06-25', location='Old city', deadlines=[{'label': 'Main Paper', 'date': '2025-11-15'}])
        html = '<h1>CVPR 2027</h1><p>Conference Venue: New Convention Center, Seattle</p><p>Conference Dates: June 20-25, 2027</p><p>Full Paper Submission: November 16, 2026 at 23:59 AoE</p>'
        result, _ = updater.refresh_record(old, datetime(2026, 7, 1, tzinfo=timezone.utc), fetch=MagicMock(return_value=html))
        self.assertEqual(result['year'], 2027)
        self.assertEqual(result['location'], 'New Convention Center, Seattle')
        self.assertEqual(result['starts_on'], '2027-06-20')
        self.assertEqual(result['deadlines'][0]['date'], '2026-11-16')
        self.assertEqual(result['deadlines'][0]['at'], '2026-11-16T23:59:00-12:00')

    def test_full_and_short_deadlines_accumulate_across_pages(self):
        htmls = ['<h1>CVPR 2027</h1><h3>Main Papers</h3><p>Full Paper Submission: November 16, 2026</p>', '<h1>CVPR 2027</h1><h3>Main Papers</h3><p>Short Paper Submission: November 23, 2026</p>']
        seed = record(deadlines=[{'label': 'Main Paper (Round 2)', 'date': '2026-09-01', 'at': None, 'status': 'confirmed'}])
        result, _ = updater.refresh_record(seed, datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=htmls))
        deadlines = {d['label']: d for d in result['deadlines']}
        self.assertEqual(deadlines['Main Paper']['date'], '2026-11-16')
        self.assertEqual(deadlines['Short Paper']['date'], '2026-11-23')
        self.assertEqual(deadlines['Main Paper (Round 2)']['date'], '2026-09-01')
        self.assertNotEqual(result['sync_status'], 'conflicting')

    def test_main_full_synonyms_replace_only_same_kind_and_preserve_short_seed(self):
        html = '<h1>CVPR 2027</h1><p>Main Paper Submission: November 16, 2026</p>'
        seed = record(deadlines=[{'label': 'Full Paper', 'date': '2026-11-15', 'at': None}, {'label': 'Short Paper', 'date': '2026-11-23', 'at': None}])
        result, _ = updater.refresh_record(seed, datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(return_value=html))
        self.assertEqual(len(result['deadlines']), 2)
        self.assertEqual({d['label']: d['date'] for d in result['deadlines']}, {'Main Paper': '2026-11-16', 'Short Paper': '2026-11-23'})

    def test_same_date_with_more_precise_clock_is_not_a_conflict(self):
        htmls = ['<h1>CVPR 2027</h1><p>Full Paper Submission: November 16, 2026 AoE</p>', '<h1>CVPR 2027</h1><p>Full Paper Submission: November 16, 2026 at 23:59 AoE</p>']
        result, _ = updater.refresh_record(record(), datetime(2026, 10, 10, tzinfo=timezone.utc), fetch=MagicMock(side_effect=htmls))
        self.assertNotEqual(result['sync_status'], 'conflicting')
        self.assertEqual(result['deadlines'][0]['at'], '2026-11-16T23:59:00-12:00')

    def test_rollover_waits_until_end_of_last_aoe_day(self):
        old = record(year=2026, ends_on='2026-06-25')
        offline = MagicMock(side_effect=OSError('offline'))
        before, _ = updater.refresh_record(old, datetime(2026, 6, 26, 11, 59, 59, tzinfo=timezone.utc), fetch=offline)
        after, _ = updater.refresh_record(old, datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc), fetch=offline)
        self.assertEqual(before['year'], 2026)
        self.assertEqual(after['year'], 2027)

    def test_security_allowlist_and_redirect_policy(self):
        self.assertTrue(updater.allowed_url('https://cvpr.thecvf.com/Conferences/2027', 'cvpr'))
        for url in ['http://cvpr.thecvf.com/', 'https://cvpr.thecvf.com.evil.test/', 'https://127.0.0.1/', 'https://user@cvpr.thecvf.com/', 'https://cvpr.thecvf.com:444/']:
            self.assertFalse(updater.allowed_url(url, 'cvpr'))
        with self.assertRaises(ValueError):
            updater.OfficialRedirect('cvpr').redirect_request(None, None, 302, '', {}, 'https://evil.test/')

    @patch.object(updater, 'build_opener')
    def test_response_size_is_bounded(self, opener):
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.headers.get.return_value = str(updater.MAX_BYTES + 1)
        opener.return_value.open.return_value = response
        with self.assertRaises(ValueError):
            updater.fetch_html('https://cvpr.thecvf.com/', 'cvpr')
        response.read.assert_not_called()

    def test_atomic_update_failure_leaves_input_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'conferences.json'
            path.write_text('{"invalid": true}')
            with self.assertRaises(ValueError):
                updater.update_file(path)
            self.assertEqual(path.read_text(), '{"invalid": true}')
