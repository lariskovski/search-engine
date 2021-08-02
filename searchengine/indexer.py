import logging

def add_to_index(index: dict, keyword: str, url: str) -> None:
    '''Populates with formatted keywords index hashtable'''
    if keyword in index:
        index[keyword].append(url)
    else:
        # logging too many keywords significantly slows down execution time
        logging.info(f"New keyword entry on {url}: {keyword}")
        index[keyword] = [url]


def add_page_to_index(index: list, url: str, content: str) -> dict:
    from .parser import PageParser
    '''Formats all page content to no-HTML-tags text and passes each word into add_to_index()'''
    parser = PageParser()
    words = parser.format_content(content).split()
    for word in words:
        add_to_index(index, word, url)
    return index
