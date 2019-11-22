import os


def save_page(filename, html):
    with open(os.path.join('.', 'tests/pages', f'{filename}.html'), 'w') as f:
        f.write(html)