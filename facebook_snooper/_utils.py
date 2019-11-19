import re


def strip_ml(text):
    return re.sub('<[^<]+?>', '', text)