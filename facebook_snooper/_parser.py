from lxml import html as lxml_html, \
                 etree
import re
import html
from . import _text


def parse_image(html_text):
    image_link = ''
    matches = re.findall(r'photoContainer.+?img.+?src="(.+?)"', html_text)
    if matches:
        image_link = html.unescape(matches[0])
    return image_link


def parse_followers(html_text):
    followers = ''
    matches = re.findall(r'Follower:.+?<', html_text)
    if matches:
        followers = matches[0][10:-1]
    return followers


def parse_intro(html_text):
    items = []
    ul_html = None

    matches = re.findall(r'intro_container_id.+?</ul', html_text)
    if matches:
        ul_html = matches[0][20:-4]

    if ul_html:
        tree = lxml_html.fromstring(ul_html)
        for intro in tree.xpath('//li/*[1]/div/div/div'):
            fragment = etree.tostring(intro).decode("utf-8")
            items.append(_text.strip_ml(fragment))           
    return items


def parse_search_result(html_text):
    results = []

    # Rip JavaScript dictionary data
    profileURIs = re.findall(r'profileURI:".+?"', html_text)
    texts = re.findall(r'text:".+?"', html_text)

    if profileURIs:
        for i, profileURI in enumerate(profileURIs):
            profile_uri = html.unescape(profileURI[12:-1])
            if not '/groups/' in profile_uri and \
            not '/events/' in profile_uri:
                profile_id = _text.get_profile_id(profile_uri)
                profile_name = texts[i][6:-1]
                results.append((profile_id, profile_name, profile_uri))
    return results