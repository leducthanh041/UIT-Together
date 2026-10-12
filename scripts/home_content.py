"""Select dated group announcements and explicitly chosen publications for Home."""
from datetime import date, timedelta
import re
from urllib.parse import urlsplit


def reviewed_news(records):
    seen = set()
    selected = []
    for item in records:
        identifier = item.get('id', '')
        if not identifier or identifier in seen:
            raise ValueError('News IDs must be present and unique')
        seen.add(identifier)
        published = item.get('date', '')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', published):
            raise ValueError(f'{identifier}: date must use YYYY-MM-DD')
        date.fromisoformat(published)
        if not item.get('title') or not item.get('description'):
            raise ValueError(f'{identifier}: title and description are required')
        if item.get('verified') is not True:
            continue
        source = urlsplit(item.get('source_url', ''))
        if source.scheme != 'https' or not source.netloc or not item.get('date_source'):
            raise ValueError(f'{identifier}: reviewed news needs an HTTPS source and date provenance')
        selected.append(item)
    return sorted(selected, key=lambda item: item['date'], reverse=True)


def selected_publications(identifiers, publications):
    if not 2 <= len(identifiers) <= 3 or len(set(identifiers)) != len(identifiers):
        raise ValueError('Select two or three distinct research highlight IDs')
    result = []
    seen = set()
    for identifier in identifiers:
        if identifier not in publications:
            raise ValueError(f'Unknown research highlight: {identifier}')
        item = publications[identifier]
        if not item.get('display_title') or not item.get('year') or not item.get('venue_name'):
            raise ValueError(f'{identifier}: highlight metadata is incomplete')
        if not (item.get('doi') or item.get('paper_url') or item.get('links')):
            raise ValueError(f'{identifier}: highlight needs a paper source')
        key = (item.get('doi') or item['display_title'].casefold(), item['venue_name'], item['year'])
        if key in seen:
            raise ValueError(f'{identifier}: the same paper is selected twice')
        seen.add(key)
        result.append(item)
    return result


def home_context(data, today=None):
    news = reviewed_news(data['news'])
    today = today or date.today()
    return {
        'copyright_year': today.year,
        'group_news': news,
        'latest_news': news[:3],
        'news_is_historical': bool(news and date.fromisoformat(news[0]['date']) < today - timedelta(days=365)),
        'research_highlights': selected_publications(data['selected_achievements'], data['publications']),
    }
