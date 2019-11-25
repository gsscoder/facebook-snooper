import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..')))
from facebook_snooper import Session


__all__ = [
    "save_current_page"
]


def save_current_page(session: Session, filename):
    html_ = str(session._browser.get_current_page())
    with open(f'./tests/pages/{filename}.html', 'w') as page:
        page.write(html_)