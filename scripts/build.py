"""Build static HTML from trusted local templates and JSON data."""
from pathlib import Path
import json
import shutil
import tempfile
import re
import unicodedata
from i18n import localize_html, localized_url, normalize
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
ROOT = Path(__file__).resolve().parent.parent

def publication_groups(data):
    """Merge exact title/venue/year duplicates for display without deleting source records."""
    unique = {}
    venues = data['venues']
    for record in data['publications'].values():
        title = record['display_title']
        key = (unicodedata.normalize('NFC', re.sub(r'\s+', ' ', title).strip().rstrip('.')).casefold(), record['venue_id'], record['year'])
        if not title or record.get('needs_metadata_review'):
            key = (record['id'], record['venue_id'], record['year'])
        if key not in unique:
            unique[key] = dict(record, citations=[], search_text='', source_ids=[])
        item = unique[key]
        if record['citation'] not in item['citations']:
            item['citations'].append(record['citation'])
        item['source_ids'].append(record['id'])
        item['doi'] = item['doi'] or record['doi']
        item['paper_url'] = item.get('paper_url') or record.get('paper_url', '')
        item['links'] = list(dict.fromkeys(item['links'] + record['links']))
        item['search_text'] = ' '.join(item['citations']) + ' ' + item['venue_name'] + ' ' + item['doi']
    grouped = {}
    for item in unique.values():
        group = grouped.setdefault(item['venue_id'], {'venue': venues[item['venue_id']], 'publications': []})
        group['publications'].append(item)
    for group in grouped.values():
        group['publications'].sort(key=lambda item: (item['year'], item['display_title']), reverse=True)
    return sorted(grouped.values(), key=lambda group: (group['venue']['type'] != 'journal', group['venue']['name'].casefold()))

def build():
    source = ROOT / "src"
    data = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (source / "data").glob("*.json")}
    # A downloaded venue cover can be added using its slug without editing templates.
    for slug, venue in data['venues'].items():
        if not venue['image']:
            for extension in ['webp', 'png', 'jpg', 'jpeg', 'svg']:
                image = source / 'assets/images/venues' / f'{slug}.{extension}'
                if image.is_file():
                    venue['image'] = f'/assets/images/venues/{image.name}'
                    break
    data['publication_groups'] = publication_groups(data)
    env = Environment(loader=FileSystemLoader(str(source)), autoescape=select_autoescape(["html"]), undefined=StrictUndefined)
    output = Path(tempfile.mkdtemp(prefix=".uit-build-", dir=ROOT))
    try:
        routes = {page['url'] for page in data['pages']}
        translations = data.get('translations', {'en': {}, 'vi': {}})
        english = dict(translations['en'], **data.get('tutorial-translations', {}))
        vietnamese = {value: key for key, value in english.items()}
        vietnamese.update(translations['vi'])
        for page in data["pages"]:
            for language, dictionary in [('en', english), ('vi', vietnamese)]:
                prefix = 'vi/' if language == 'vi' else ''
                target = output / (prefix + page["source"])
                target.parent.mkdir(parents=True, exist_ok=True)
                localized_page = dict(page)
                lookup = {normalize(key): value for key, value in dictionary.items()}
                localized_page['title'] = lookup.get(normalize(page['title']), page['title'])
                localized_page['hero'] = [lookup.get(normalize(text), text) for text in page['hero']]
                if 'redirect_to' in page:
                    localized_page['redirect_to'] = localized_url(page['redirect_to'], language, routes)
                html = env.get_template("pages/" + page["source"]).render(page=localized_page, language=language, **data)
                html = localize_html(html, language, dictionary, routes, page['url'])
                target.write_text(html, encoding="utf-8")
        # Preserve public asset routes during migration.
        for name, destination in [("css", "assets/css"), ("fonts", "assets/fonts"), ("images", "assets/images"), ("pdfs", "assets/pdfs"), ("themes", "assets/themes"), ("js", "js")]:
            path = source / "assets" / name
            if path.exists():
                shutil.copytree(path, output / destination, dirs_exist_ok=True)
        shutil.copytree(source / "static", output, dirs_exist_ok=True)
        (output / ".nojekyll").touch()
        old = ROOT / "dist"
        if old.exists():
            shutil.rmtree(old)
        output.rename(old)
        print(f"Built {len(data['pages']) * 2} pages (English + Vietnamese) → {old}")
        return old
    except Exception:
        shutil.rmtree(output)
        raise

if __name__ == "__main__":
    build()
