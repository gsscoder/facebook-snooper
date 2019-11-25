from facebook_snooper import Session


__all__ = [
    "save_current_page"
]


def save_login(session: Session):
    session._browser.open('https://www.facebook.com')
    save_current_page(session, 'login')


def save_current_page(session: Session, filename):
    html_ = str(session._browser.get_current_page())
    with open(f'./tests/pages/{filename}.html', 'w') as page:
        page.write(html_)