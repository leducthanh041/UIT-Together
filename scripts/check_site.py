"""Check generated routes, local assets, data and regressions against migration baseline."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import sys
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

def check():
    output = ROOT / 'dist'
    data = ROOT / 'src/data'
    pages = json.loads((data / 'pages.json').read_text())
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
            target = output / unquote(parts.path).lstrip('/') if parts.path.startswith('/') else path.parent / unquote(parts.path)
            if target.is_file() or (target / 'index.html').is_file() or target.with_suffix('.html').is_file():
                continue
            issue = {'page':page['source'], 'url':url}
            missing.append(issue)
            original_path = parts.path[3:] if page['language'] == 'vi' and parts.path.startswith('/vi/') else parts.path
            if (page['original_source'], original_path) not in baseline:
                new.append(issue)
    members = json.loads((data/'members.json').read_text())
    assert len({m['id'] for m in members}) == len(members)
    publications = json.loads((data/'publications.json').read_text())
    assert all(k == v['id'] and v['citation'] for k,v in publications.items())
    private = [str(p.relative_to(output)) for p in output.rglob('*') if p.is_file() and (p.suffix in ['.enc','.py'] or p.name in ['.env','Gemfile','SKILL.md'])]
    assert not private, private
    report = {'pages':len(generated_pages),'source_pages':len(pages),'languages':['en','vi'],'members':len(members),'students':sum(len(c['names']) for c in json.loads((data/'cohorts.json').read_text())),'publication_records':len(publications),'existing_missing_links':missing,'new_missing_links':new,'private_files':private}
    (ROOT/'docs/site-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f"Checked {len(generated_pages)} pages, {len(publications)} publication records. Missing links: {len(missing)}; new: {len(new)}")
    return 1 if new else 0
if __name__ == '__main__':
    sys.exit(check())
