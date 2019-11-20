import re

def strip_ml(text):
    return re.sub(r'<[^<]+?>', '', text)


def get_profile_id(uri):
    chunk = uri.split('/')[3]
    if 'profile.php?id=' in uri:
         chunk = chunk.split('?')[1].split('=')[1]
    return chunk