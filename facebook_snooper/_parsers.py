from lxml import html, \
                 etree
from . import _utils


def parse_intro(html_text):
    items = []

    start_ix = html_text.find('intro_container_id')
    start_ix = html_text.find('<ul', start_ix)
    end_ix = html_text.find('</ul', start_ix)
    ul_html = html_text[start_ix : end_ix + 5]

    tree = html.fromstring(ul_html)

    for intro in tree.xpath('//li/*[1]/div/div/div'):
        fragment = etree.tostring(intro).decode("utf-8")
        items.append(_utils.strip_ml(fragment))
    return items


def parse_search_result(html_text):
    profiles = []
    ix = 0
    while True:
        start_ix = html_text.find('profileURI:"', ix)
        if start_ix < 0:
            break
        end_ix = html_text.find('"', start_ix + 12)
        if end_ix > 0:
            profile_info = html_text[start_ix : end_ix + 1]
            profile_uri = profile_info[12:len(profile_info)-1]
            if not '/groups/' in profile_uri and \
               not '/events/' in profile_uri:
                profile_id = profile_uri.split('/')[3]
                profiles.append((profile_id, profile_uri))
        ix = end_ix
    return profiles