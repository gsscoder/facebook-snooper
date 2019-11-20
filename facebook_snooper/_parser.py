from lxml import html, \
                 etree
import re


def strip_ml(text):
    return re.sub(r'<[^<]+?>', '', text)


def parse_followers(html_text):
    followers = ''
    matches = re.findall(r'Follower:.+?<', html_text)
    if matches:
        followers = matches[0][10:-1]
    return followers


def parse_intro(html_text):
    items = []
    ul_html = None

    start_ix = html_text.find('intro_container_id')
    if start_ix > -1:
        start_ix = html_text.find('<ul', start_ix)
        if start_ix > -1:
            end_ix = html_text.find('</ul', start_ix)
            if end_ix > -1:
                ul_html = html_text[start_ix : end_ix + 5]

    if ul_html:
        tree = html.fromstring(ul_html)
        for intro in tree.xpath('//li/*[1]/div/div/div'):
            fragment = etree.tostring(intro).decode("utf-8")
            items.append(strip_ml(fragment))           
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