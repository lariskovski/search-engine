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
