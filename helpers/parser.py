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

if __name__ == "__main__":
    import requests
    url = 'https://udacity.github.io/cs101x/urank/'
    page_content = requests.get(url).text
    parser = PageParser()
    print(format_content(parser, page_content))
