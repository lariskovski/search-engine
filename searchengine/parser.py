from html.parser import HTMLParser

class PageParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.clean_content = []


    def handle_data(self, data):
        # import translate # C code library
        # import string
        if data != '':
            # Translate function removes all punctuation. Installation: pip install translate
            # PROS: reduces drastically index keyword count
            # CONS: breaks http urls intended to be represented as text (even removing only dots)
            # data = data.strip().lower().translate(str.maketrans('', '', string.punctuation))

            data = data.strip().lower()
            self.clean_content.append(data)


    def format_content(self, raw_content: str) -> str:
        '''HTML Formatter removes html tags for string'''
        self.feed(raw_content)
        formatted_content = " ".join(self.clean_content)
        return formatted_content
