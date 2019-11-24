import re
import html
from lxml import html as lxml_html, \
                 etree
from ._text import strip_ml


class Parser:
    def parse_image(self, name, soup):
        image_link = ''
        matches = soup.find_all('img', alt=name)
        if len(matches) > 0:
            image = matches[0]
            image_link = image.attrs['src'] if 'src' in image.attrs else ''
        return image_link

    def parse_info(self, soup):
        items = \
            self._parse_info('work', soup)
        items.extend(
            self._parse_info('education', soup))
        items.extend(
            self._parse_info('living', soup))
        return items

    def parse_search_result(self, soup):
        results = []
        container = soup.find_all('div', attrs={'id': 'BrowseResultsContainer'})[0]
        for a in container.find_all('a'):
            if 'href' in a.attrs:
                href = a.attrs['href']
                id_ = self._get_profile_id(href)
                link = f'https://m.facebook.com{href}'
                texts = []
                for div in a.find_all('div'):
                    text = div.get_text()
                    # Avoid duplicates
                    if len(text) > 0 and text not in texts and \
                        '/groups/' not in href and '/events/' not in href:
                        texts.append(text)
                if len(texts) > 0:
                    results.append((id_, texts, link))
        return results

    def _parse_info(self, type_, soup):
        items = []
        html_ = str(soup)
        tree = lxml_html.fromstring(html_.encode('utf-8'))
        for link in tree.xpath(f"//div[@id='{type_}']//a"):
            if not link.text is None:
                items.append(link.text)
        return items
    
    def _get_profile_id(self, uri_part):
        matches = re.findall(r'(?<=\=).+?(?=&)', uri_part)
        if matches:
            return matches[0]
        matches = re.findall(r'(?<=/).+?(?=\?)', uri_part)
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