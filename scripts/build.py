"""Build static HTML from trusted local templates and JSON data."""
from pathlib import Path
import json
import argparse
import shutil
import tempfile
import re
import unicodedata
from i18n import localize_html, localized_url, normalize
from group_statistics import group_statistics
from site_paths import normalize_base_path, prefix_html, prefix_css
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

def build(base_path=""):
    base_path = normalize_base_path(base_path)
    source = ROOT / "src"
    data = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (source / "data").glob("*.json")}
    destination_root = ROOT / 'dist'
    destination_root.parent.mkdir(parents=True, exist_ok=True)
    # A downloaded venue cover can be added using its slug without editing templates.
    for slug, venue in data['venues'].items():
        if not venue['image']:
            for extension in ['webp', 'png', 'jpg', 'jpeg', 'svg']:
                image = source / 'assets/images/venues' / f'{slug}.{extension}'
                if image.is_file():
                    venue['image'] = f'/assets/images/venues/{image.name}'
                    break
    data['publication_groups'] = publication_groups(data)
    data['group_stats'] = group_statistics(data, (source / 'partials/datasets-content.html').read_text(encoding='utf-8'))
    env = Environment(loader=FileSystemLoader(str(source)), autoescape=select_autoescape(["html"]), undefined=StrictUndefined)
    output = Path(tempfile.mkdtemp(prefix=".uit-build-", dir=destination_root.parent))
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
                html = env.get_template("pages/" + page["source"]).render(page=localized_page, language=language, base_path=base_path, **data)
                html = localize_html(html, language, dictionary, routes, page['url'])
                target.write_text(html, encoding="utf-8")
        # Preserve public asset routes during migration.
        for name, destination in [("css", "assets/css"), ("fonts", "assets/fonts"), ("images", "assets/images"), ("pdfs", "assets/pdfs"), ("themes", "assets/themes"), ("js", "js")]:
            path = source / "assets" / name
            if path.exists():
                shutil.copytree(path, output / destination, dirs_exist_ok=True)
        shutil.copytree(source / "static", output, dirs_exist_ok=True)
        calendar_output = output / 'assets/data/conferences.json'
        calendar_output.parent.mkdir(parents=True, exist_ok=True)
        calendar_output.write_text(json.dumps(data.get('conferences', {}), ensure_ascii=False), encoding='utf-8')
        for path in output.rglob('*.html'):
            path.write_text(prefix_html(path.read_text(encoding='utf-8'), base_path), encoding='utf-8')
        if base_path:
            for path in output.rglob('*.css'):
                path.write_text(prefix_css(path.read_text(encoding='utf-8'), base_path), encoding='utf-8')
        (output / ".nojekyll").touch()
        old = destination_root
        if old.exists():
            shutil.rmtree(old)
        output.rename(old)
        print(f"Built {len(data['pages']) * 2} pages (English + Vietnamese) → {old}")
        return old
    except Exception:
        shutil.rmtree(output)
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-path", default="", help="GitHub Pages project path; empty for local/custom domain")
    build(parser.parse_args().base_path)
