def parse_image(page, name):
    image_link = ''
    matches = page.find_all('img', alt=name)
    if len(matches) > 0:
        image = matches[0]
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
    matches = page.find_all('div', attrs={'id': 'BrowseResultsContainer'})
    if len(matches) == 0:
        return []
    results = []
    container = matches[0]
    for a in container.find_all('a'):
        if 'href' in a.attrs:
            href = a.attrs['href']
            id_ = _get_profile_id(href)
            link = f'{base_url}{href}'
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
    texts = []
    matches = page.find_all('div', attrs={'id': type_})
    if len(matches) > 0:
        links = matches[0].find_all('a')
        for link in links:
            text = link.get_text()
            if link.get_text():
                texts.append(text)
    return texts


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