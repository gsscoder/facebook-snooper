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
    followers_re = re.compile(r'frankbruninyt/followers.*people', re.MULTILINE)
    matches = followers_re.findall(html_text)
    if matches:
        followers = _text.sanitize_followers(matches[0])
        followers = followers if followers.isdigit() else ''
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
            info = html.unescape(_text.strip_ml(fragment))
            items.append(info)           
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