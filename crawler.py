import requests

seed = "http://pudim.com.br/"

def get_page_content(url):
    return requests.get(url).text

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
            print(page)
            union(to_crawl, get_all_links(get_page_content(page)))
            crawled.append(page)
    return crawled

# print(crawl(seed))
crawl_web(seed)

# print(get_all_links(get_page_content(seed)))