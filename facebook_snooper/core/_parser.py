import re
import html
from lxml import html as lxml_html, \
                 etree
from ._text import strip_ml


class Parser:
    def parse_image(self, name, html_):
        image_link = ''
        tree = lxml_html.fromstring(html_.encode('utf-8'))
        image = tree.xpath(f"//img[@alt='{name}']")
        if not image is None:
            image_link = image[0].attrib['src']
        return image_link

    def parse_info(self, html_):
        items = \
            self._parse_info('work', html_)
        items.extend(
            self._parse_info('education', html_))
        items.extend(
            self._parse_info('living', html_))
        return items

    def parse_search_result(self, html_text):
        results = []
        # Rip JavaScript dictionary data
        profileURIs = re.findall(r'profileURI:".+?"', html_text)
        texts = re.findall(r'text:".+?"', html_text)
        if profileURIs:
            for i, profileURI in enumerate(profileURIs):
                profile_uri = html.unescape(profileURI[12:-1])
                if not '/groups/' in profile_uri and \
                   not '/events/' in profile_uri:
                    profile_id = self._get_profile_id(profile_uri)
                    profile_name = texts[i][6:-1]
                    results.append((profile_id, profile_name, profile_uri))
        return results

    def _parse_info(self, type_, html_):
        items = []
        tree = lxml_html.fromstring(html_.encode('utf-8'))
        for link in tree.xpath(f"//div[@id='{type_}']//a"):
            if not link.text is None:
                items.append(link.text)
        return items

    def _get_profile_id(self, uri):
        chunk = uri.split('/')[3]
        if 'profile.php?id=' in uri:
            chunk = chunk.split('?')[1].split('=')[1]
        return chunk

    def _sanitize_followers_1(self, text):
        # Remove trailing HTML
        followers = text[:-6][9:].strip()
        # Remove thousands separator for every culture
        return followers.replace('.', '').replace(',', '')

    def _sanitize_followers_2(self, text):
        followers = ''
        if '>' in text:
            # Remove trailing HTML
            followers = text[text.find('>') + 1:-7]
            # Remove thousands separator for every culture
            followers = followers.replace('.', '').replace(',', '')
        return followers