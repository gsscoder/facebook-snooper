from lxml import html, \
                 etree
import re
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
    profileURIs = re.findall(r'profileURI:".+?"', html_text)
    for profileURI in profileURIs:
        profile_uri = profileURI[12:-1]
        if not '/groups/' in profile_uri and \
           not '/events/' in profile_uri:
            profile_id = profile_uri.split('/')[3]
            profiles.append((profile_id, profile_uri))
    return profiles