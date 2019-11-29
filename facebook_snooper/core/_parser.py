__all__ = [
    'InfoTypes',
    'ResultTypes'
]


class InfoTypes:
    WORK = 0
    EDUCATION = 1
    LIVING = 2

    def __init__(self):
        pass

    @staticmethod
    def tostring(type_):
        if type_ == InfoTypes.WORK:
            return 'work'
        elif type_ == InfoTypes.EDUCATION:
            return 'education'
        elif type_ == InfoTypes.LIVING:
            return 'living'

    @staticmethod
    def fromstring(str_):
        if str_ == 'work':
            return InfoTypes.WORK
        elif str_ == 'education':
            return InfoTypes.EDUCATION
        elif str_ == 'living':
            return InfoTypes.LIVING


class ResultTypes:
    PROFILE = 0
    GROUP = 1
    EVENT = 2
    VIDEO = 3

    def __init__(self):
        pass

    @staticmethod
    def tostring(type_):
        if type_ == ResultTypes.PROFILE:
            return 'profile'
        elif type_ == ResultTypes.GROUP:
            return 'group'
        elif type_ == ResultTypes.EVENT:
            return 'event'
        elif type_ == ResultTypes.VIDEO:
            return 'video'


def parse_image(page, name):
    image_link = ''
    image = page.select_one(f"img[alt='{name}']")
    if image:
        image_link = image.attrs['src'] if 'src' in image.attrs else ''
    return image_link


def parse_info(page):
    items = \
        _parse_info(page, 'work')
    items.extend(
        _parse_info(page, 'education'))
    items.extend(
        _parse_info(page, 'living'))
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
                if type_ == ResultTypes.PROFILE else None
            link = href if 'http' in href else f'{base_url}{href}'
            texts = []
            # Video lacks profile ID and descriptions
            if type_ != ResultTypes.VIDEO:          
                for div in a.find_all('div'):
                    text = div.get_text()
                    # Avoid duplicates
                    if len(text) > 0 and text not in texts:
                        texts.append(text)
            if len(texts) > 0 or type_ == ResultTypes.VIDEO:
                results.append((type_, id_, texts, link))
    return results


def _parse_info(page, type_):
    infos = []
    div = page.select_one(f'div#{type_}')
    if div:
        for link in div.find_all('a'):
            text = link.get_text()
            if text:
                infos.append((InfoTypes.fromstring(type_), text))
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