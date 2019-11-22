import re


def strip_ml(markup):
    return re.sub(r'<[^<]+?>', '', markup)