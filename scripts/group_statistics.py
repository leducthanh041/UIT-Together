"""Build-time counts from the same public content rendered by the website."""
from html.parser import HTMLParser
import unicodedata


def name_key(value):
    return unicodedata.normalize('NFC', ' '.join(value.split())).casefold()


class DatasetNames(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.label = []
        self.names = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h4' and 'media-heading' in attrs.get('class', '').split():
            self.active = True
            self.label = []
        if tag == 'small' and self.active:
            self.names.add(name_key(''.join(self.label)))
            self.active = False  # The year is not part of the dataset identity.

    def handle_data(self, data):
        if self.active:
            self.label.append(data)

    def handle_endtag(self, tag):
        if tag == 'h4' and self.active:
            self.names.add(name_key(''.join(self.label)))
            self.active = False


def group_statistics(data, dataset_html):
    names = {name_key(m['name']) for m in data['members']}
    names.update(name_key(n) for c in data['cohorts'] for n in c['names'])
    datasets = DatasetNames()
    datasets.feed(dataset_html)
    groups = data['publication_groups']
    return {
        'participants': len(names - {''}),
        'papers': sum(len(g['publications']) for g in groups),
        'venues': sum(g['venue']['type'] in ('journal', 'conference') for g in groups),
        'datasets': len(datasets.names - {''}),
    }
