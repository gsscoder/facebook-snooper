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
    matches = page.find_all('div', attrs={'id': 'BrowseResultsContainer'})
    if len(matches) == 0:
        return []
    results = []
    container = matches[0]
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
    texts = []
    div = page.select_one(f'div#{type_}')
    if div:
        for link in div.find_all('a'):
            text = link.get_text()
            if text:
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