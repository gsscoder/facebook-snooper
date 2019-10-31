from mechanicalsoup import StatefulBrowser
from lxml import html
from lxml import etree
import re


__all__ = ['log_in', 'get_intro']


_base_url = 'https://www.facebook.com'


def log_in(username, password):
    """Log in to facebook with username and password."""
    global _browser

    try:
        _browser = StatefulBrowser()
        _browser.addHeaders = [('User-Agent', 'Firefox'), \
            ('Accept-Language', 'en-US,en;q=0.5')]
        
        _browser.open(_base_url)

        _browser.select_form('form[id="login_form"]')
        _browser['email'] = username
        _browser['pass'] =  password
        
        _browser.submit_selected()
        return True
    except:
        return False 

def get_intro(profile_id):
    """Retrieve introductory informations from given profile."""
    try:
        url = f'{_base_url}/{profile_id}'
        
        _browser.open(url)

        profile_html = str(_browser.get_current_page())
        return _extract_intro(profile_html)
    except:
        return None

def _extract_intro(profile_html):
    items = []

    start_ix = profile_html.find('intro_container_id')
    start_ix = profile_html.find('<ul', start_ix)
    end_ix = profile_html.find('</ul', start_ix)
    ul_html = profile_html[start_ix : end_ix + 5]

    tree = html.fromstring(ul_html)

    for link in tree.xpath('//li'):
        div0 = next(link.iterchildren())
        for div1 in div0.iterchildren():
            for div2 in div1.iterchildren():
                for elem in div2.iterchildren():
                    if elem.tag == 'div':
                        fragment = etree.tostring(elem).decode("utf-8")
                        items.append(_strip_ml(fragment))
    return items

def _strip_ml(text):
    return re.sub('<[^<]+?>', '', text)