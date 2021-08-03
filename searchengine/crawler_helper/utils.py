
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
    # if '?' not in url:
    #     return url, end_quote
    # else:
    #     return None, 0


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

def union(p: list, q: list) -> list:
    '''Unites two lists by adding unique elements from the second to the first one.'''
    for item in q:
        if item not in p:
            p.append(item)
    return p