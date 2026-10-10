#!/usr/bin/env python3
"""Conservative, bounded official-source conference refresh (stdlib only)."""
import argparse
import copy
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 2 * 1024 * 1024
TIMEOUT = 8
MAX_PAGES = 5
FAMILIES = {
    'cvpr': ('cvpr.thecvf.com',), 'iccv': ('iccv.thecvf.com',), 'wacv': ('wacv.thecvf.com',),
    'iclr': ('iclr.cc',), 'neurips': ('neurips.cc',), 'aaai': ('aaai.org',),
    'sigir': ('sigir.org',), 'icmr': ('acmicmr.org',), 'mmm': ('mmm2027.net', 'mmm2027.org', 'mmm2026.org'),
    'kse': ('kse-conf.org', 'kse-conferences.org'), 'rivf': ('rivf.net', 'rivf.org'), 'miccai': ('miccai.org',),
    'mm': ('acmmm.org',), 'acmmm': ('acmmm.org',), 'ecir': (),
}
YEAR_HOST = {
    'sigir': r'(?:www\.)?sigir20\d{2}\.org', 'icmr': r'(?:www\.)?(?:acm)?icmr20\d{2}\.org',
    'mmm': r'(?:www\.)?mmm20\d{2}\.(?:org|net)', 'miccai': r'(?:www\.)?miccai20\d{2}\.org',
    'kse': r'kse20\d{2}\.kse-conferences\.org',
    'rivf': r'(?:www\.)?rivf20\d{2}\.org',
    'ecir': r'(?:www\.)?ecir20\d{2}\.co\.uk',
    'mm': r'20\d{2}\.acmmm\.org', 'acmmm': r'20\d{2}\.acmmm\.org',
}
MONTHS = {name.lower(): number for number, names in enumerate([
    ['Jan', 'January'], ['Feb', 'February'], ['Mar', 'March'], ['Apr', 'April'], ['May'],
    ['Jun', 'June'], ['Jul', 'July'], ['Aug', 'August'], ['Sep', 'Sept', 'September'],
    ['Oct', 'October'], ['Nov', 'November'], ['Dec', 'December']], 1) for name in names}
MONTH_RE = '|'.join(sorted(MONTHS, key=len, reverse=True))
DATE_RE = re.compile(rf"\b(?P<m>{MONTH_RE})\.?\s+(?P<d>\d{{1,2}})(?:st|nd|rd|th)?(?:\s*[-–—]\s*(?P<end>\d{{1,2}})(?:st|nd|rd|th)?)?\s*,?\s*['’]?(?P<y>20\d{{2}}|\d{{2}})\b", re.I)
DAY_RE = re.compile(rf'\b(?P<d>\d{{1,2}})(?:st|nd|rd|th)?\s+(?P<m>{MONTH_RE})\.?\s*,?\s*(?P<y>20\d{{2}})\b', re.I)
ISO_RE = re.compile(r'\b(20\d{2}-\d{2}-\d{2})(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2}))?(?!\d)')


def allowed_url(url, conference_id):
    try:
        parts = urlsplit(url)
        host = (parts.hostname or '').lower()
        return (parts.scheme == 'https' and parts.port in (None, 443) and not parts.username and not parts.password
                and not parts.fragment and not any(ord(c) < 32 for c in url)
                and (host.removeprefix('www.') in FAMILIES.get(conference_id, ())
                     or bool(re.fullmatch(YEAR_HOST.get(conference_id, r'(?!)'), host))))
    except (ValueError, TypeError):
        return False


class OfficialRedirect(HTTPRedirectHandler):
    def __init__(self, conference_id):
        self.conference_id = conference_id
        super().__init__()

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl, self.conference_id):
            raise ValueError('Redirect outside the conference official host allowlist.')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_html(url, conference_id):
    if not allowed_url(url, conference_id):
        raise ValueError('Source is not an allowlisted HTTPS official conference URL.')
    request = Request(url, headers={'User-Agent': 'UIT-Together-ConferenceUpdater/1.0', 'Accept': 'text/html,application/ld+json'})
    with build_opener(OfficialRedirect(conference_id)).open(request, timeout=TIMEOUT) as response:
        if response.status != 200:
            raise ValueError('Unexpected HTTP status.')
        size = response.headers.get('Content-Length')
        if size and (not size.isdigit() or int(size) > MAX_BYTES):
            raise ValueError('Response exceeds the size limit.')
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError('Response exceeds the size limit.')
        return body.decode(response.headers.get_content_charset() or 'utf-8', errors='replace')


class SourceHTML(HTMLParser):
    """Retain row/paragraph evidence and titles, ignore deleted/hidden/script text."""
    BLOCKS = {'tr', 'p', 'li', 'h1', 'h2', 'h3', 'h4', 'div'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.blocks = []
        self.titles = []
        self.links = []
        self.structured = []
        self.script = None
        self.heading = ''
        self.contexts = {}
        self.location_blocks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        hidden = tag in {'s', 'del', 'strike', 'style'} or 'hidden' in attrs or attrs.get('aria-hidden') == 'true'
        inherited = self.stack[-1]['hidden'] if self.stack else False
        if tag == 'script':
            self.script = [] if attrs.get('type', '').lower() == 'application/ld+json' else None
            hidden = True
        forbidden_location = tag in {'footer', 'address', 'nav'} or bool(re.search(r'footer|contact|copyright', attrs.get('class', '') + ' ' + attrs.get('id', ''), re.I)) or bool(self.stack and self.stack[-1]['forbidden_location'])
        node = {'forbidden_location': forbidden_location, 'tag': tag, 'parts': [], 'hidden': hidden or inherited, 'datetime': attrs.get('datetime', '')}
        if tag not in {'br', 'img', 'meta', 'link', 'input', 'hr', 'wbr', 'source', 'area', 'base', 'embed', 'param', 'track', 'col'}:
            self.stack.append(node)
        if tag == 'a' and not node['hidden'] and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'time' and attrs.get('datetime') and not node['hidden']:
            self.handle_data(' ' + attrs['datetime'] + ' ')
        if tag in {'td', 'th', 'br'}:
            self.handle_data(' | ')

    def handle_data(self, data):
        if self.stack and self.stack[-1]['tag'] == 'script':
            if self.script is not None:
                self.script.append(data)
            return
        if self.stack and not self.stack[-1]['hidden']:
            for node in self.stack:
                node['parts'].append(data)

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i]['tag'] == tag), None)
        if index is None:
            return
        node = self.stack[index]
        del self.stack[index:]
        content = ' '.join(''.join(node['parts']).split())
        if tag == 'script' and self.script is not None:
            try:
                self.structured.append(json.loads(''.join(self.script)))
            except (ValueError, TypeError):
                pass
            self.script = None
        if tag in {'title', 'h1'} and content:
            self.titles.append(content)
        if tag in {'h2', 'h3', 'h4'} and content:
            self.heading = content
        if tag in self.BLOCKS and content and len(content) <= 700:
            self.blocks.append(content)
            self.contexts[content] = self.heading
            if not node['forbidden_location']:
                self.location_blocks.append(content)


def parse_dates(text):
    result = []
    for match in ISO_RE.finditer(text):
        try:
            parsed = date.fromisoformat(match.group(1))
            result.append((parsed, parsed, match.group(0)))
        except ValueError:
            pass
    if result:
        return result
    covered = []
    ranges = [
        re.compile(rf'\b(?P<m>{MONTH_RE})\.?\s+(?P<d>\d{{1,2}})(?:st|nd|rd|th)?\s*[-–—]\s*(?P<em>{MONTH_RE})\.?\s+(?P<ed>\d{{1,2}})(?:st|nd|rd|th)?\s*,?\s*(?P<y>20\d{{2}})\b', re.I),
        re.compile(rf'\b(?P<d>\d{{1,2}})\s+(?P<m>{MONTH_RE})\.?\s*[-–—]\s*(?P<ed>\d{{1,2}})\s+(?P<em>{MONTH_RE})\.?\s*,?\s*(?P<y>20\d{{2}})\b', re.I),
    ]
    for pattern in ranges:
        for match in pattern.finditer(text):
            try:
                start = date(int(match['y']), MONTHS[match['m'].lower()], int(match['d']))
                end = date(int(match['y']), MONTHS[match['em'].lower()], int(match['ed']))
                if start <= end:
                    result.append((start, end, match.group(0)))
                    covered.append(match.span())
            except ValueError:
                pass
    for pattern in [DATE_RE, DAY_RE]:
        for match in pattern.finditer(text):
            if any(start <= match.start() < end for start, end in covered):
                continue
            try:
                year = int(match['y'])
                year += 2000 if year < 100 else 0
                start = date(year, MONTHS[match['m'].lower()], int(match['d']))
                end_day = match.groupdict().get('end') or match['d']
                end = date(year, start.month, int(end_day))
                if end >= start:
                    result.append((start, end, match.group(0)))
            except ValueError:
                pass
    return result


def explicit_time(text, on_date):
    iso = re.search(r'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})', text)
    if iso:
        try:
            value = datetime.fromisoformat(iso[0].replace('Z', '+00:00'))
            return value.isoformat() if value.date() == on_date else None
        except ValueError:
            return None
    clock = re.search(r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)?', text, re.I)
    if not clock:
        return None
    offset = None
    if re.search(r'\bAoE\b|Anywhere on Earth', text, re.I):
        offset = -12 * 60
    else:
        zone = re.search(r'\bUTC(?:\s*([+-])\s*(\d{1,2})(?::(\d{2}))?)?\b', text, re.I)
        if zone:
            offset = (int(zone[2] or 0) * 60 + int(zone[3] or 0)) * (-1 if zone[1] == '-' else 1)
    if offset is None or abs(offset) > 14 * 60:
        return None
    hour, minute, second = int(clock[1]), int(clock[2]), int(clock[3] or 0)
    if clock[4]:
        if not 1 <= hour <= 12:
            return None
        hour = hour % 12 + (12 if clock[4].upper() == 'PM' else 0)
    try:
        return datetime.combine(on_date, datetime.min.time()).replace(hour=hour, minute=minute, second=second, tzinfo=timezone(timedelta(minutes=offset))).isoformat()
    except ValueError:
        return None


def structured_events(value):
    if isinstance(value, list):
        for item in value:
            yield from structured_events(item)
    elif isinstance(value, dict):
        kind = value.get('@type', [])
        if kind == 'Event' or isinstance(kind, list) and 'Event' in kind:
            yield value
        yield from structured_events(value.get('@graph', []))



def location_text(value):
    if not isinstance(value, str):
        return None
    value = ' '.join(value.split()).strip(' |')
    if not value or len(value) > 240 or re.search(r'\b(?:TBA|TBD|contact|copyright|submission|deadline)\b|conference dates|to be (?:announced|determined|confirmed)|not announced', value, re.I):
        return None
    return value


def deadline_keys(label):
    """Main/full/regular/research are one track; short papers are distinct."""
    label = str(label)
    round_match = re.search(r'round\s*(\d+)', label, re.I)
    round_number = round_match[1] if round_match else ''
    short = bool(re.search(r'\bshort\b', label, re.I))
    main = bool(re.search(r'\bmain\b|\bfull\b|\bregular\b|\bresearch\b', label, re.I))
    if short and main:
        return [('main', round_number), ('short', round_number)]
    if short:
        return [('short', round_number)]
    if main or re.search(r'\bpaper', label, re.I):
        return [('main', round_number)]
    return [(label.casefold().strip(), round_number)]


def deadline_label(key):
    kind, round_number = key
    label = 'Short Paper' if kind == 'short' else 'Main Paper'
    return label + (' (Round ' + round_number + ')' if round_number else '')


def conflicting_deadlines(rows):
    if len({row.get('date') for row in rows}) > 1:
        return True
    instants = set()
    for row in rows:
        if row.get('at'):
            try:
                instants.add(datetime.fromisoformat(row['at'].replace('Z', '+00:00')).astimezone(timezone.utc).isoformat())
            except ValueError:
                instants.add(row['at'])
    return len(instants) > 1


def parse_page(html, conference, source):
    page = SourceHTML()
    page.feed(html)
    year, acronym = int(conference['year']), conference['acronym']
    # Navigation/footer years alone are not evidence of the edition.
    edition = re.compile(rf'\b{re.escape(acronym)}\s*[-:]?\s*{year}\b|\b{year}\s*{re.escape(acronym)}\b', re.I)
    date_title = re.compile(rf'\b{year}\b.*(?:Dates|Deadlines)|(?:Dates|Deadlines).*\b{year}\b', re.I)
    short_edition = re.compile(rf'\b{re.escape(acronym)}-{year % 100:02d}\b', re.I)
    confirmed_edition = any(short_edition.search(title) or edition.search(title) or date_title.search(title) and '/Conferences/' + str(year) + '/' in source for title in page.titles)
    update = {'deadlines': []}
    for blob in page.structured:
        for event in structured_events(blob):
            if not edition.search(str(event.get('name', ''))):
                continue
            confirmed_edition = True
            starts = parse_dates(str(event.get('startDate', '')))
            ends = parse_dates(str(event.get('endDate', '')))
            if starts and ends and starts[0][0].year == year and ends[0][0] >= starts[0][0]:
                update.update(starts_on=starts[0][0].isoformat(), ends_on=ends[0][0].isoformat(), date_status='confirmed')
            location = event.get('location', {})
            if isinstance(location, dict) and location_text(location.get('name')):
                update['location'] = location_text(location['name'])
    if source == conference.get('series_url'):
        confirmed_edition = confirmed_edition or any(edition.search(b) and parse_dates(b) for b in page.blocks)
    if not confirmed_edition:
        raise ValueError('No title/structured evidence for the requested conference edition.')
    locations = set()
    for block in page.location_blocks:
        if re.search(r'contact|footer|copyright', page.contexts.get(block, ''), re.I):
            continue
        match = re.match(r'^(?:Conference (?:Venue|Location)|Venue|Location)\s*[:|]\s*(.+)$', block.strip(' |'), re.I)
        if match:
            location = location_text(match[1])
            if location:
                locations.add(location)
    if len(locations) == 1 and 'location' not in update:
        update['location'] = next(iter(locations))
    deadlines = {}
    meetings = []
    for block in page.blocks:
        dates = parse_dates(block)
        if not dates:
            continue
        context = page.contexts.get(block, '')
        tentative = bool(re.search(r'\bproposed\b|\btentative\b|subject to change', block + ' ' + context, re.I)) or any(re.search(r'(?:dates|deadlines).{0,80}(?:proposed|tentative)|(?:proposed|tentative).{0,80}(?:dates|deadlines)', b, re.I) for b in page.blocks)
        if any(re.search(r'all (?:submission )?deadlines.{0,100}(?:AoE|Anywhere on Earth)', b, re.I) for b in page.blocks):
            block += ' AoE'
        if (re.search(r'\b(?:main conference|conference dates|meeting dates|conference sessions)\b', block + ' ' + context, re.I) or edition.search(block) and any(a != b for a, b, _ in dates)) and not re.search(r'submission|deadline|notification', block, re.I):
            for starts, ends, _ in dates:
                if starts.year == year and ends.year == year:
                    meetings.append((starts, ends, tentative))
        if re.search(r'workshop|tutorial|supplement|camera.ready|notification|review|registration|rebuttal|abstract', block + ' ' + context, re.I):
            continue
        if not re.search(r'(?:full|main|regular|research|short)\s+papers?\s+(?:submission|deadline)|papers?\s+submission\s+(?:deadline|due)|(?:submission|submissions)\s+deadline', block, re.I):
            continue
        if not re.search(r'papers?|full|regular|research', block + ' ' + context, re.I):
            continue
        # Repeated nested blocks are harmless, but multiple non-deleted dates are ambiguous.
        unique_dates = {item[0] for item in dates}
        if len(unique_dates) != 1:
            continue
        day = dates[-1][0]
        if day.year not in {year - 1, year}:
            continue
        round_match = re.search(r'round\s*(\d)', block + ' ' + context, re.I)
        kind_evidence = block if re.search(r'\b(?:short|full|regular|research|main)\b', block, re.I) else block + ' ' + context
        kinds = deadline_keys(kind_evidence)
        # Context includes evidence, not a UI label; normalize labels to explicit kinds.
        kinds = [(kind, round_match[1] if round_match else '') for kind, _ in kinds]
        deadline = {'at': explicit_time(block, day), 'date': day.isoformat(),
                    'zone': 'AoE' if re.search(r'\bAoE\b|Anywhere on Earth', block, re.I) else None,
                    'status': 'tentative' if tentative else 'confirmed', 'source': source}
        for key in kinds:
            label = deadline_label(key)
            item = dict(deadline, label=label)
            if label in deadlines and deadlines[label]['date'] != item['date']:
                deadlines.pop(label)
                deadlines['ambiguous:' + label] = None
            elif 'ambiguous:' + label not in deadlines:
                deadlines[label] = item
    update['deadlines'] = [value for value in deadlines.values() if value]
    if meetings and 'ends_on' not in update:
        starts, ends = min(item[0] for item in meetings), max(item[1] for item in meetings)
        if (ends - starts).days <= 30:
            update.update(starts_on=starts.isoformat(), ends_on=ends.isoformat(), date_status='tentative' if any(item[2] for item in meetings) else 'confirmed')
    return update, page.links


def edition_urls(conference):
    cid, year = conference['id'], int(conference['year'])
    template = conference.get('source_template')
    templated = []
    if isinstance(template, str):
        try:
            candidate = template.format(year=year)
            if allowed_url(candidate, cid):
                templated.append(candidate)
        except (KeyError, ValueError):
            pass
    if cid in {'cvpr', 'wacv', 'iccv'}:
        return list(dict.fromkeys(templated + [f'https://{cid}.thecvf.com/Conferences/{year}/Dates', f'https://{cid}.thecvf.com/Conferences/{year}']))
    if cid in {'iclr', 'neurips'}:
        return [f'https://{cid}.cc/Conferences/{year}/Dates', f'https://{cid}.cc/Conferences/{year}']
    if cid == 'aaai':
        return [f'https://aaai.org/conference/aaai/aaai-{year % 100:02d}/']
    if cid in {'mm', 'acmmm'}:
        return templated + [f'https://{year}.acmmm.org/']
    if cid == 'mmm':
        return [f'https://mmm{year}.net/']
    if cid == 'rivf':
        return [f'https://rivf{year}.org/']
    if cid == 'kse':
        return [f'https://kse{year}.kse-conferences.org/']
    if cid == 'ecir':
        return [f'https://www.ecir{year}.co.uk/']
    if cid in {'sigir', 'icmr', 'miccai'}:
        return [f'https://icmr{year}.org/'] if cid == 'icmr' else [f'https://{cid}{year}.org/']
    return templated


def refresh_record(record, now, fetch=fetch_html):
    current = copy.deepcopy(record)
    now_string = now.astimezone(timezone.utc).isoformat(timespec='seconds')
    try:
        ended = bool(current.get('ends_on')) and datetime.combine(date.fromisoformat(current['ends_on']), datetime.max.time(), tzinfo=timezone(timedelta(hours=-12))) < now
    except ValueError:
        ended = False
    if ended:
        current['year'] += int(current.get('cadence') or (2 if current['id'] == 'iccv' else 1))
        current.update(starts_on=None, ends_on=None, location='', date_status='unannounced', deadlines=[], source_urls=edition_urls(current), website='', last_success_at=None)
        current['notes_en'] = 'Next edition: awaiting verified official dates and location.'
        current['notes_vi'] = 'Kỳ tiếp theo: đang chờ ngày và địa điểm từ nguồn chính thức.'
    candidates = list(dict.fromkeys([*edition_urls(current), *current.get('source_urls', []), current.get('website', ''), current.get('series_url', '')]))
    successes = 0
    evidence = []
    errors = []
    observed_dates = set()
    observed_deadlines = {}
    accumulated_deadlines = {}
    for deadline in current.get('deadlines', []):
        keys = deadline_keys(deadline.get('label', ''))
        for key in keys:
            item = copy.deepcopy(deadline)
            if len(keys) > 1:
                item['label'] = deadline_label(key)
            accumulated_deadlines[key] = item
    for url in candidates:
        if len(evidence) + len(errors) >= MAX_PAGES:
            break
        if not url or not allowed_url(url, current['id']):
            continue
        try:
            parsed, links = parse_page(fetch(url, current['id']), current, url)
            # Success is actual extracted evidence, not simply HTTP 200.
            useful = bool(parsed.get('deadlines') or parsed.get('ends_on') or parsed.get('location'))
            if parsed.get('ends_on'):
                observed_dates.add((parsed.get('starts_on'), parsed['ends_on']))
            for deadline in parsed.get('deadlines', []):
                for key in deadline_keys(deadline['label']):
                    observed_deadlines.setdefault(key, []).append(deadline)
            if useful:
                for key in ['starts_on', 'ends_on', 'location', 'date_status']:
                    if key in parsed:
                        current[key] = parsed[key]
                successes += 1
                current['website'] = current.get('website') or url
                evidence.append(url)
            else:
                errors.append('No unambiguous dates on ' + url)
            # Follow only date/CFP pages on official hosts, never general external links.
            for link in links:
                target = urljoin(url, link)
                if allowed_url(target, current['id']) and re.search(r'/date(?:s)?(?:[/?.]|$)|call.for.papers|cfp|/cfc(?:[/?.]|$)|important', target, re.I) and target not in candidates:
                    candidates.append(target)
        except Exception as error:
            errors.append(type(error).__name__ + ': ' + str(error)[:160])
    # Full conference spans legitimately contain shorter main-session spans.
    enclosing = [span for span in observed_dates if all(span[0] <= other[0] and span[1] >= other[1] for other in observed_dates)]
    if len(observed_dates) > 1 and enclosing:
        observed_dates = {enclosing[0]}
        current.update(starts_on=enclosing[0][0], ends_on=enclosing[0][1])
    conflict_keys = set()
    for key, rows in observed_deadlines.items():
        if conflicting_deadlines(rows):
            accumulated_deadlines.pop(key, None)
            conflict_keys.add(key)
        else:
            item = copy.deepcopy(max(rows, key=lambda row: (bool(row.get('at')), bool(row.get('zone')))))
            if any(row.get('status') == 'tentative' for row in rows):
                item['status'] = 'tentative'
            accumulated_deadlines[key] = item
    current['deadlines'] = list(accumulated_deadlines.values())
    conflicts = len(observed_dates) > 1 or bool(conflict_keys)
    if len(observed_dates) > 1:
        current.update(starts_on=None, ends_on=None, date_status='unannounced')
    if conflicts:
        current['notes_en'] = 'Official sources disagree; conflicting dates are hidden pending verification.'
        current['notes_vi'] = 'Nguồn chính thức không thống nhất; ẩn các ngày mâu thuẫn để chờ xác minh.'
    current['checked_at'] = now_string
    if successes:
        current['last_success_at'] = now_string
        current['sync_status'] = 'conflicting' if conflicts else ('partial' if errors else 'ok')
        current['source_urls'] = list(dict.fromkeys([*evidence, *current.get('source_urls', [])]))
        if ended and not conflicts and current.get('ends_on') and current.get('location'):
            current['notes_en'] = ''
            current['notes_vi'] = ''
    else:
        current['sync_status'] = 'pending' if ended or not current.get('last_success_at') else 'stale'
    return current, errors


def update_file(path, now=None, fetch=fetch_html):
    now = now or datetime.now(timezone.utc)
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not isinstance(data.get('conferences'), list):
        raise ValueError('Expected conferences JSON object with a conferences list.')
    refreshed, errors = [], []
    def refresh(conference):
        return refresh_record(conference, now, fetch)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for conference, (current, warnings) in zip(data['conferences'], pool.map(refresh, data['conferences'])):
            refreshed.append(current)
            errors.extend(conference['id'] + ': ' + warning for warning in warnings)
    data.update(conferences=refreshed, updated_at=now.astimezone(timezone.utc).isoformat(timespec='seconds'), timezone='Asia/Ho_Chi_Minh')
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT / 'src/data/conferences.json')
    args = parser.parse_args(argv)
    # Restrict writes to the agreed data target, not arbitrary command-line destinations.
    if args.data.resolve() != (ROOT / 'src/data/conferences.json').resolve():
        parser.error('Only src/data/conferences.json can be updated.')
    try:
        warnings = update_file(args.data)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('Conference data unchanged: ' + str(error), file=sys.stderr)
        return 1
    for warning in warnings:
        print('Conference refresh warning: ' + warning, file=sys.stderr)
    # Offline/provider failures are nonfatal: stale/pending state is an honest usable result.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
