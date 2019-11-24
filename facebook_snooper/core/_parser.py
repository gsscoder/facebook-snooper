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

    def parse_search_result(self, soup):
        results = []
        container = soup.find_all('div', id='BrowseResultsContainer')[0]
        for a in container.find_all('a'):
            if 'href' in a.attrs:
                href = a.attrs['href']
                id_ = self._get_profile_id(href)
                link = f'https://m.facebook.com{href}'
                texts = []
                for div in a.find_all('div'):
                    text = div.get_text()
                    # Avoid duplicates
                    if len(text) > 0 and text not in texts:
                        texts.append(text)
                if len(texts) > 0:
                    results.append((id_, texts, link))
        return results

    def _parse_info(self, type_, html_):
        items = []
        tree = lxml_html.fromstring(html_.encode('utf-8'))
        for link in tree.xpath(f"//div[@id='{type_}']//a"):
            if not link.text is None:
                items.append(link.text)
        return items
    
    def _get_profile_id(self, uri_part):
        matches = re.findall('(?<=\=).+?(?=&)', uri_part)
        if matches:
            return matches[0]
        matches = re.findall('(?<=/).+?(?=\?)', uri_part)
        if matches:
            return matches[0]
        return ''

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