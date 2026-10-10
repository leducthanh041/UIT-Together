"""Static bilingual HTML localization; never translate code or research identifiers."""
from html import escape
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import urlsplit, urlunsplit
import re


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

    def translate(self, text):
        normalized = normalize(text)
        translated = self.translations.get(normalized)
        if translated is None:
            return text
        return re.sub(r'\S(?:[\s\S]*\S)?', lambda _: translated, text, count=1)

    def handle_starttag(self, tag, attrs):
        original = dict(attrs)
        protected = any(item[1] for item in self.stack) or tag in {'pre', 'code', 'script', 'style'} or original.get('translate') == 'no'
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
            self.stack.append((tag, protected))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')
        for index in range(len(self.stack)-1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if self.stack and self.stack[-1][0] in {'script','style'}:
            self.parts.append(data)
        elif any(item[1] for item in self.stack):
            self.parts.append(escape(data, quote=False))
        else:
            self.parts.append(escape(self.translate(data), quote=False))

    def handle_entityref(self, name): self.parts.append('&' + name + ';')
    def handle_charref(self, name): self.parts.append('&#' + name + ';')
    def handle_comment(self, data): self.parts.append('<!--' + data + '-->')
    def handle_decl(self, decl): self.parts.append('<!' + decl + '>')


def localize_html(html, language, translations, routes, page_url):
    parser = Localizer(language, {normalize(k): v for k,v in translations.items()}, routes, page_url)
    parser.feed(html)
    parser.close()
    return ''.join(parser.parts)
