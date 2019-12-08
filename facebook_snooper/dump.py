from .core._parser import InfoTypes, ResultTypes


def dump_search(data, pretty=False):
    for type_, id_, texts, link in data:
        type_ = ResultTypes.tostring(type_) if pretty else type_
        link_ = _shorten(link, 50) if pretty else link
        print(f'{type_} {id_} {link_}')
        for text in texts:
            print(f'  {_shorten(text, 70)}')


def dump_info(data, pretty=False):
    name, image_link, texts = data
    image_link_ = _shorten(image_link, 70) if pretty else image_link
    print(f'{name}\nImage: {image_link_}')
    for type_, descs in texts:
        print(f'  {type_} {descs}')

def _shorten(text, max_len):
    if len(text) > max_len:
        return f'{text[:50]}...'
    else:
        return text