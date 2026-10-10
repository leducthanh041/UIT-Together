"""Root and GitHub project-site URLs, without rewriting external links or anchors."""
import re


def normalize_base_path(value):
    value = (value or '').strip()
    if value in ('', '/'):
        return ''
    if not value.startswith('/') or not re.fullmatch(r'/[A-Za-z0-9_.\-/]+', value):
        raise ValueError('Base path must be a site path such as /UIT-Together.')
    if any(part in ('.', '..') for part in value.split('/')) or '//' in value:
        raise ValueError('Base path cannot contain traversal or empty segments.')
    return value.rstrip('/')


def site_url(value, base_path):
    if not base_path or not value.startswith('/') or value.startswith('//'):
        return value
    if value == base_path or value.startswith(base_path + '/'):
        return value
    return base_path + value


def prefix_html(text, base_path):
    if not base_path:
        return text
    pattern = re.compile(r'\b(href|src|poster|action|data-src)=("|\')([^"\']*)\2', re.I)
    text = pattern.sub(lambda m: m[1] + '=' + m[2] + site_url(m[3], base_path) + m[2], text)
    text = re.sub(r'(\bcontent=(?:"|\')[^"\']*\burl=)(/[^"\']*)', lambda m: m[1] + site_url(m[2], base_path), text, flags=re.I)
    return prefix_css(text, base_path)


def prefix_css(text, base_path):
    return re.sub(r'(url\(\s*["\']?)(/(?!/)[^\s)"\']*)', lambda m: m[1] + site_url(m[2], base_path), text)
