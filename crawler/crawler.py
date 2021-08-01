import logging

def get_page_content(url) -> str:
    try:
        import requests
        return requests.get(url).text
    except:
        logging.warn(f"Couldnt get content from address {url}")
        return ""

def get_next_target(page: str) -> tuple:
    start_link = page.find('href=')

    # if the link tag sequence is not found, find returns a -1
    if start_link == -1:
        # return the error codes of None, 0 now and skip the rest!
        return None, 0

    # Get url start and end index inside double quotes after href tag
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1 : end_quote]
    return url, end_quote


def get_all_links(page: str) -> list:
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url != None:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def add_to_index(index: dict, keyword: str, url: str) -> None:
    if keyword in index:
        index[keyword].append(url)
    else:
        logging.info(f"New keyword entry on {url}: {keyword}")
        index[keyword] = [url]


def add_page_to_index(index: list, url: str, content: str) -> dict:
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
    return index
