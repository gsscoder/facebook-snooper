__all__ = [
    'InfoTypes'
]


class InfoTypes:
    WORK_INFO = 'work'
    EDUCATION_INFO = 'education'
    LIVING_INFO = 'living'

    def __init__(self):
        pass


def parse_image(page, name):
    image_link = ''
    image = page.select_one(f"img[alt='{name}']")
    if image:
        image_link = image.attrs['src'] if 'src' in image.attrs else ''
    return image_link


def parse_info(page):
    items = \
        _parse_info(page, InfoTypes.WORK_INFO)
    items.extend(
        _parse_info(page, InfoTypes.EDUCATION_INFO))
    items.extend(
        _parse_info(page, InfoTypes.LIVING_INFO))
    return items


def parse_search(page, base_url):
    container = page.select_one('div#BrowseResultsContainer')
    if not container:
        return []
    results = []
    for a in container.find_all('a'):
        if 'href' in a.attrs:
            href = a.attrs['href']
            id_ = _get_profile_id(href)
            link = href if 'http' in href else f'{base_url}{href}'
            texts = []
            for div in a.find_all('div'):
                text = div.get_text()
                # Avoid duplicates
                if len(text) > 0 and text not in texts and \
                    '/groups/' not in href and '/events/' not in href \
                    and '/video_redirect/' not in href:
                    texts.append(text)
            if len(texts) > 0:
                results.append((id_, texts, link))
    return results


def _parse_info(page, type_):
    infos = []
    div = page.select_one(f'div#{type_}')
    if div:
        for link in div.find_all('a'):
            text = link.get_text()
            if text:
                infos.append((type_, text))
    return infos


def _get_profile_id(uri_part):
    import re
    # m.facebook.com/profile.php?id=[profile.id]
    # m.facebook.com/profile.php?id=[profile.id]?refid=n
    # m.facebook.com/profile.php?id=[profile.id]&refid=n
    matches = re.findall(r'(?<=\?id=).+?(?=$|\?|&)', uri_part)
    if matches:
        return matches[0]

    # m.facebook.com/[profile.id]
    # m.facebook.com/[profile.id]/?refid=n
    # m.facebook.com/[profile.id]?refid=n
    # m.facebook.com/[profile.id]&refid=n
    matches = re.findall(r'(?<=/).*?(?=$|/|\?|&)', uri_part)
    if matches:
        return matches[0]
    return ''