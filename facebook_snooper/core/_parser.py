import re
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
        texts = []
        matches = soup.find_all('div', attrs={'id': type_})
        if len(matches) > 0:
            links = matches[0].find_all('a')
            for link in links:
                text = link.get_text()
                if link.get_text():
                    texts.append(text)
        return texts
    
    def _get_profile_id(self, uri_part):
        matches = re.findall(r'(?<=\=).+?(?=&)', uri_part)
        if matches:
            return matches[0]
        matches = re.findall(r'(?<=/).+?(?=\?)', uri_part)
        if matches:
            return matches[0]
        return ''