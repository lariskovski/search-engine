from html.parser import HTMLParser

class PageParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.clean_content = []


    def handle_data(self, data):
        data = data.strip()
        if data != '':
            self.clean_content.append(data)


def format_content(instance: object, raw_content: str) -> str:
    parser = PageParser()
    parser.feed(raw_content)
    formatted_content = " ".join(parser.clean_content)
    return formatted_content


def union(p: list, q: list) -> None:
    '''Unites two lists by adding unique elements from the second to the first one.'''
    for item in q:
        if item not in p:
            p.append(item)
    return p
