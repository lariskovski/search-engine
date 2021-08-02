from html.parser import HTMLParser

class PageParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.clean_content = []


    def handle_data(self, data):
        data = data.strip()
        if data != '':
            self.clean_content.append(data)


    def format_content(self, raw_content: str) -> str:
        '''HTML Formatter removes html tags for string'''
        self.feed(raw_content)
        formatted_content = " ".join(self.clean_content)
        return formatted_content


def union(p: list, q: list) -> list:
    '''Unites two lists by adding unique elements from the second to the first one.'''
    for item in q:
        if item not in p:
            p.append(item)
    return p
