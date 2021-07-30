# ============
# Dummy Web Crawler
# ============

import requests

# seed = "http://pudim.com.br/"
# Dummy pages content
def get_page_content(url) -> str:
    if url == "https://desserts.com/index.html":
        return 'Choose your favorite dessert! <a href="http://pudim.com.br"> <a href="https://gelly.com">'
    elif url == "http://pudim.com.br":
        return requests.get("http://pudim.com.br").text
    elif url == "https://gelly.com":
        return "<h1>Im a Gelly lovers page<\h1>"
    else:
        raise NotImplementedError(f"No valid return for url {url}")
    # return requests.get(url).text


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


def get_all_links(page: str) -> None:
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url != None:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(p: list, q: list) -> None:
    '''Unites two lists by adding unique elements from the second to the first one.'''
    for item in q:
        if item not in p:
            p.append(item)
    return p


def crawl_web(seed):
    ''' Starts crawling pages from the seed using Depth-first Search'''
    to_crawl =  [seed]
    crawled = []
    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            try:
                content = get_page_content(page)
                add_page_to_index(index, page, content)
                union(to_crawl, get_all_links(content))
                crawled.append(page)
            except Exception as e:
                print(f"Couldnt get {page}", e)

    return crawled


def add_page_to_index(index: list, url: str, content: str) -> list:
    words = content.split()
    for word in words:
        is_word_in_keywords = False
        for entry in index:
            if word == entry[0]:
                entry[1].append(url)
                is_word_in_keywords = True
        if not is_word_in_keywords:
            index.append([word, [url]])
    return index


def lookup(index:list,keyword:str) -> list:
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []


if __name__ == "__main__":
    index = []
    crawl_web('https://desserts.com/index.html')
    # print(index)
    print(lookup(index, 'lovers'))