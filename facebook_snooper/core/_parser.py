__all__ = [
    'InfoTypes',
    'ResultTypes'
]


class InfoTypes:
    WORK = 'work'
    EDUCATION = 'education'
    LIVING = 'living'

    def __init__(self):
        pass


class ResultTypes:
    PROFILE = 'profile'
    GROUP = 'group'
    EVENT = 'event'
    VIDEO = 'video'

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
        _parse_info(page, InfoTypes.WORK)
    items.extend(
        _parse_info(page, InfoTypes.EDUCATION))
    items.extend(
        _parse_info(page, InfoTypes.LIVING))
    return items


def parse_search(page, base_url):
    container = page.select_one('div#BrowseResultsContainer')
    if not container:
        return []
    results = []
    for a in container.find_all('a'):
        if 'href' in a.attrs:
            href = a.attrs['href']
            type_ = _get_profile_type(href)
            id_ = _get_profile_id(href) \
                if type_ == ResultTypes.PROFILE else ''
            link = href if 'http' in href else f'{base_url}{href}'
            texts = []
            for div in a.find_all('div'):
                text = div.get_text()
                # Avoid duplicates
                if len(text) > 0 and text not in texts:
                    texts.append(text)
            if len(texts) > 0:
                results.append((type_, id_, texts, link))
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


def _get_profile_type(uri_part):
    if '/groups/' in uri_part:
        return ResultTypes.GROUP
    elif '/events/' in uri_part:
        return ResultTypes.EVENT
    elif '/video_redirect/' in uri_part:
        return ResultTypes.VIDEO
    return ResultTypes.PROFILE