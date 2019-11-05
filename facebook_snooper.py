from mechanicalsoup import StatefulBrowser, \
                           LinkNotFoundError
from lxml import html, etree
import re
import os.path


__all__ = ['log_in', 'get_intro']
__version__ = '0.1.0'


_base_url = 'https://www.facebook.com'


def log_in(username, password):
    """Log in to facebook with username and password."""
    try:
        _open_login_url(username, password)

        _browser.select_form('form[id="login_form"]')
        _browser['email'] = username
        _browser['pass'] =  password
        
        _browser.submit_selected()
        return _in_profile()
    except:
        raise Exception(f'Unable to login "{username}" into facebook.') 


def get_intro(profile_id):
    """Retrieve introductory informations from given profile."""
    try:
        return _extract_intro(_get_intro_html(profile_id))
    except:
        return None


def _open_login_url(username, password):
    global _browser

    _browser = StatefulBrowser()
    _browser.addHeaders = [('User-Agent', 'Firefox'), \
        ('Accept-Language', 'en-US,en;q=0.5')]

    _browser.open(_base_url) 


def _get_login_html(username, password):
    _open_login_url(username, password)

    return str(_browser.get_current_page())


def _get_intro_html(profile_id):
    url = f'{_base_url}/{profile_id}'
    
    _browser.open(url)

    return str(_browser.get_current_page())


def _get_search_html(query):
    _browser.select_form('form[action="/search/top/"]')
    _browser['q'] = query

    _browser.submit_selected()
    return str(_browser.get_current_page())

def _in_profile():
    try:
        _browser.select_form('form[action="/search/top/"]')
        return True
    except LinkNotFoundError:
        return False

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


def _extract_search_result(search_html):
    return []


def _strip_ml(text):
    return re.sub('<[^<]+?>', '', text)


def _test_load_html(filename):
    with open(os.path.join('.', 'test-data', f'{filename}.html'), 'r') as f:
        return f.read() 


def _test_save_html(filename, text):
    with open(os.path.join('.', 'test-data', f'{filename}.html'), 'w') as f:
        f.write(text)