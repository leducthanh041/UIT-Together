"""Check generated routes, local assets, data and regressions against migration baseline."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import sys
import argparse
from site_paths import normalize_base_path
ROOT = Path(__file__).resolve().parent.parent
class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ['href', 'src']:
            if attrs.get(key):
                self.urls.append(attrs[key])

def check(base_path=""):
    base_path = normalize_base_path(base_path)
    output = ROOT / 'dist'
    data = ROOT / 'src/data'
    def read_data(name):
        return json.loads((data / (name + '.json')).read_text())
    pages = read_data('pages')
    baseline = {(p['page'], urlsplit(p['url']).path) for p in json.loads((ROOT / 'docs/baseline-missing-links.json').read_text())}
    missing, new = [], []
    generated_pages = [dict(page, source=('vi/' if language == 'vi' else '') + page['source'], original_source=page['source'], language=language) for page in pages for language in ['en', 'vi']]
    for page in generated_pages:
        path = output / page['source']
        if not path.is_file():
            new.append({'page':page['source'], 'url':'MISSING PAGE'})
            continue
        text = path.read_text()
        assert '{% ' not in text and '{{ publications' not in text, path
        parser = Links(); parser.feed(text)
        for url in parser.urls:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            local_path = parts.path
            if base_path and local_path.startswith('/'):
                if local_path == base_path or local_path.startswith(base_path + '/'):
                    local_path = local_path[len(base_path):] or '/'
                else:
                    new.append({'page': page['source'], 'url': url, 'reason': 'Outside project base path'})
                    continue
            target = output / unquote(local_path).lstrip('/') if local_path.startswith('/') else path.parent / unquote(local_path)
            if target.is_file() or (target / 'index.html').is_file() or target.with_suffix('.html').is_file():
                continue
            issue = {'page':page['source'], 'url':url}
            missing.append(issue)
            original_path = local_path[3:] if page['language'] == 'vi' and local_path.startswith('/vi/') else local_path
            if (page['original_source'], original_path) not in baseline:
                new.append(issue)
    members = read_data('members')
    assert len({m['id'] for m in members}) == len(members)
    publications = read_data('publications')
    assert all(k == v['id'] and v['citation'] for k,v in publications.items())
    private = [str(p.relative_to(output)) for p in output.rglob('*') if p.is_file() and (p.suffix in ['.enc','.py'] or p.name in ['.env','Gemfile','SKILL.md'])]
    assert not private, private
    report = {'pages':len(generated_pages),'source_pages':len(pages),'languages':['en','vi'],'members':len(members),'students':sum(len(c['names']) for c in read_data('cohorts')),'publication_records':len(publications),'existing_missing_links':missing,'new_missing_links':new,'private_files':private}
    (ROOT/'docs/site-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f"Checked {len(generated_pages)} pages, {len(publications)} publication records. Missing links: {len(missing)}; new: {len(new)}")
    return 1 if new else 0
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-path", default="")
    sys.exit(check(parser.parse_args().base_path))
