"""Static bilingual HTML localization; never translate code or research identifiers."""
from html import escape
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import urlsplit, urlunsplit
import re


HEADING_TAGS = {'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
SMALL_WORDS = {
    'en': set('a an the and as at but by for from in into nor of on or over per '
              'so than through to under up upon via versus vs with without yet'.split()),
    'vi': set('và của cho trong trên dưới với từ đến tới về qua bằng ở như hoặc '
              'hay mà nhưng để bởi tại theo'.split()),
}
IDENTIFIER_CLASSES = {
    'member-name', 'contact-card', 'venue-heading', 'paper-title', 'paperbox',
    'publication-title', 'citation', 'journal', 'titlebox',
}
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)


def title_case(text, language='en', first=True, last=True):
    """Capitalize heading words while preserving acronyms and mixed-case names."""
    words = list(WORD.finditer(text))
    small = SMALL_WORDS.get(language, SMALL_WORDS['en'])
    index = 0

    def replace(match):
        nonlocal index
        word = match.group()
        boundary = (first and index == 0) or (last and index == len(words)-1)
        index += 1
        # AI, WSI, MMDetection, BibTeX and similar identifiers retain their case.
        if word.isupper() or any(char.isupper() for char in word[1:]):
            return word
        if word.casefold() in small and not boundary:
            return word.lower()
        return word[:1].upper() + word[1:]

    return WORD.sub(replace, text)


def normalize(text):
    return ' '.join(text.split())


def localized_url(url, language, routes):
    parts = urlsplit(url)
    if language != 'vi' or parts.scheme or parts.netloc or not parts.path.startswith('/'):
        return url
    if parts.path not in routes:
        return url
    return urlunsplit(('', '', '/vi' + parts.path, parts.query, parts.fragment))


class Localizer(HTMLParser):
    def __init__(self, language, translations, routes, page_url):
        super().__init__(convert_charrefs=True)
        self.language, self.translations, self.routes, self.page_url = language, translations, routes, page_url
        self.parts, self.stack = [], []
        self.headings = []

    def finish_heading(self, tag):
        if not self.headings or self.headings[-1]['tag'] != tag:
            return
        heading = self.headings.pop()
        nodes = heading['nodes']
        word_nodes = [i for i, (_, text, _) in enumerate(nodes) if WORD.search(text)]
        if heading['protected'] or not word_nodes:
            return
        # Remove a final sentence period even when inline markup splits the heading.
        # Preserve ellipses and protected code/identifier fragments.
        visible = ''.join(text for _, text, _ in nodes).rstrip()
        if visible.endswith('.') and not visible.endswith('..'):
            for i in range(len(nodes)-1, -1, -1):
                part, text, protected = nodes[i]
                if text.strip():
                    if not protected:
                        nodes[i] = (part, re.sub(r'\.(\s*)$', r'\1', text), protected)
                    break
        for i, (part, text, protected) in enumerate(nodes):
            if not protected:
                self.parts[part] = escape(title_case(
                    text, self.language, first=i == word_nodes[0], last=i == word_nodes[-1]
                ), quote=False)

    def translate(self, text):
        normalized = normalize(text)
        translated = self.translations.get(normalized)
        if translated is None:
            return text
        return re.sub(r'\S(?:[\s\S]*\S)?', lambda _: translated, text, count=1)

    def handle_starttag(self, tag, attrs):
        original = dict(attrs)
        protected = any(item[1] for item in self.stack) or tag in {'pre', 'code', 'script', 'style'} or original.get('translate') == 'no'
        identifier = any(item[2] for item in self.stack) or bool(
            IDENTIFIER_CLASSES.intersection(original.get('class', '').split())
        )
        if tag in HEADING_TAGS:
            self.headings.append({'tag': tag, 'nodes': [], 'protected': protected or identifier or (
                self.page_url.startswith('/papers/paper/') and tag in {'h1', 'title'}
            )})
        converted = []
        for name, value in attrs:
            if value is None:
                converted.append(name)
                continue
            if name in {'placeholder', 'aria-label', 'alt', 'title'} and not protected:
                value = self.translate(value)
            if name == 'content' and original.get('name') == 'description':
                value = self.translate(value)
            if name == 'src' and value.startswith('./assets/'):
                value = value[1:]
            if name == 'href' and 'data-language-link' not in original and original.get('rel') not in {'alternate'}:
                if not urlsplit(value).scheme and not urlsplit(value).netloc and not value.startswith(('/', '#', '?')):
                    # Resolve historic relative page links against the English route.
                    from posixpath import normpath
                    base = PurePosixPath(self.page_url) if self.page_url.endswith('/') else PurePosixPath(self.page_url).parent
                    path = normpath(str(base / urlsplit(value).path))
                    candidate = urlunsplit(('', '', path, urlsplit(value).query, urlsplit(value).fragment))
                    value = localized_url(candidate, self.language, self.routes) if path in self.routes else value
                else:
                    value = localized_url(value, self.language, self.routes)
            if tag == 'html' and name == 'lang':
                value = self.language
            converted.append(f'{name}="{escape(value, quote=True)}"')
        self.parts.append('<' + tag + (' ' + ' '.join(converted) if converted else '') + '>')
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append((tag, protected, identifier))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        self.finish_heading(tag)
        self.parts.append(f'</{tag}>')
        for index in range(len(self.stack)-1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        protected = any(item[1] for item in self.stack)
        text = data if protected else self.translate(data)
        if self.headings:
            self.headings[-1]['nodes'].append((len(self.parts), text, protected))
        if self.stack and self.stack[-1][0] in {'script','style'}:
            self.parts.append(data)
        elif any(item[1] for item in self.stack):
            self.parts.append(escape(data, quote=False))
        else:
            self.parts.append(escape(text, quote=False))

    def handle_entityref(self, name): self.parts.append('&' + name + ';')
    def handle_charref(self, name): self.parts.append('&#' + name + ';')
    def handle_comment(self, data): self.parts.append('<!--' + data + '-->')
    def handle_decl(self, decl): self.parts.append('<!' + decl + '>')


def localize_html(html, language, translations, routes, page_url):
    parser = Localizer(language, {normalize(k): v for k,v in translations.items()}, routes, page_url)
    parser.feed(html)
    parser.close()
    return ''.join(parser.parts)
