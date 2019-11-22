import re

def strip_ml(text):
    return re.sub(r'<[^<]+?>', '', text)


def sanitize_title(title):
    # Handle cases like 'Some One - Home'
    if '-' in title:
        return title.split('-')[0].strip()
    return title


def sanitize_followers(text):
    followers = ''
    if '>' in text:
        # Remove trailing HTML and
        followers = text[text.find('>') + 1:-7]
        # Remove thousands separator for every culture
        followers = followers.replace('.', '').replace(',', '')
    return followers