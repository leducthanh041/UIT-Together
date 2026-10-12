"""Member roster, grouping, public templates and future-cohort regressions."""
import copy
from datetime import date
import json
from pathlib import Path
import re
import unittest
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

ROOT = Path(__file__).resolve().parents[1]


class MemberLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {p.stem: json.loads(p.read_text()) for p in (ROOT / 'src/data').glob('*.json')}
        cls.data['copyright_year'] = date.today().year
        cls.env = Environment(loader=FileSystemLoader(ROOT / 'src'), undefined=StrictUndefined, autoescape=select_autoescape(['html']))
        cls.page = next(p for p in cls.data['pages'] if p['url'] == '/team/')

    def render(self, lang='en', **overrides):
        return self.env.get_template('pages/team/index.html').render(page=self.page, language=lang, **dict(self.data, **overrides))

    def test_supervisor_pairs_and_roles_inside_cards(self):
        supervisors = [m for m in self.data['members'] if m['section'] == 'Supervisor']
        self.assertEqual([m['name'] for m in supervisors], ['Khang Nguyen', 'Tam Nguyen', 'Khanh Duy Nguyen', 'Doanh C. Bui', 'Tung Minh Tran', 'Nguyen Duy Vo', 'Hiep Nguyen', 'Dung Truong', 'My Hoan Nguyen', 'Long Duong'])
        html = self.render()
        section = html.split('id="supervisors"', 1)[1].split('id="current-members"', 1)[0]
        self.assertEqual(re.findall(r'data-member-id="([^"]+)"', section), [m['id'] for m in supervisors])
        self.assertRegex(section, r'data-member-id="member-001"[\s\S]+class="member-role">Leader')
        self.assertRegex(section, r'data-member-id="member-002"[\s\S]+class="member-role">Collaborator')

    def test_current_members_and_pending_bios_in_both_languages(self):
        current = [m for m in self.data['members'] if m['section'] == 'Current Members']
        self.assertEqual(len(current), 7)
        self.assertNotIn('Doanh C. Bui', [m['name'] for m in current])
        for lang, pending in [('en', 'A short introduction will be added'), ('vi', 'Giới thiệu sẽ được cập nhật')]:
            html = self.render(lang).split('id="current-members"', 1)[1].split('id="former-members"', 1)[0]
            for member in current:
                self.assertIn(member['name'], html)
            self.assertEqual(html.count('class="member-bio-section"'), 7)
            self.assertEqual(html.count(pending), 6)
            self.assertIn('listen to Nobody New before talking to me.', html)
            self.assertEqual(html.count('member-initials'), 3)
        for member in self.data['members']:
            if member['image']:
                self.assertTrue((ROOT / 'src' / member['image'].lstrip('/')).is_file())

    def test_former_cohorts_keep_all_names_and_original_order(self):
        html = self.render().split('id="former-members"', 1)[1]
        previous = -1
        for cohort in self.data['cohorts']:
            if int(cohort['cohort'][1:]) > 2022:
                continue
            position = html.index('data-cohort="' + cohort['cohort'] + '"')
            self.assertGreater(position, previous)
            previous = position
            region = html[position:].split('</ol>', 1)[0]
            names = re.findall(r'<li[^>]*>([^<]+)</li>', region)
            self.assertEqual(names, cohort['names'])

    def test_new_cohort_is_current_and_does_not_duplicate_profile(self):
        cohorts = [{'cohort': 'K2024', 'names': ['A New Member']}, {'cohort': 'K2023', 'names': ['Lê Đức Thành', 'Another Member']}] + self.data['cohorts']
        html = self.render(cohorts=cohorts)
        current = html.split('id="current-members"', 1)[1].split('id="former-members"', 1)[0]
        self.assertIn('A New Member', current)
        self.assertIn('Another Member', current)
        self.assertEqual(current.count('>Lê Đức Thành<'), 1)
        self.assertNotIn('data-cohort="K2024"', html.split('id="former-members"', 1)[1])
        members = copy.deepcopy(self.data['members'])
        target = next(m for m in members if m['name'] == 'Lê Đức Thành')
        target.update(bio_en='Researching robust vision.', bio_vi='Nghiên cứu thị giác máy tính.')
        self.assertIn('Researching robust vision.', self.render(members=members))
        self.assertIn('Nghiên cứu thị giác máy tính.', self.render('vi', members=members))

    def test_no_member_pagination_and_papers_unchanged(self):
        html = self.render()
        self.assertNotIn('data-page-size', html)
        self.assertNotIn('data-page-by', html)
        self.assertIn('class="member-scroll"', html)
        self.assertIn('/js/members.js', html)
        self.assertEqual(html.count('data-member-chapter'), 3)
        paper_page = next(p for p in self.data['pages'] if p['url'] == '/papers/')
        data = dict(self.data, publication_groups=[])
        papers = self.env.get_template('pages/papers/index.html').render(page=paper_page, language='en', **data)
        self.assertIn('data-page-size="10"', papers)
        self.assertNotIn('/js/members.js', papers)


if __name__ == '__main__':
    unittest.main()
