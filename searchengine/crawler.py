from .utils import timer
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

logging.basicConfig(level=logging.INFO)

@timer
def crawl_web(seed: str) -> tuple:
    ''' Starts crawling pages from the seed using Depth-first Search'''
    from .parser import union
    from .indexer import add_page_to_index

    to_crawl =  [seed]
    crawled = []

    index = {}

    graph = {} # used for ranking
    
    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            logging.info(f"Crawling page: {page}")
            content = get_page_content(page)

            add_page_to_index(index, page, content)

            links_on_page = get_all_links(content)
            logging.info(f"Links found on page: {links_on_page}")

            graph[page] = links_on_page

            # include unique links found on page to queue
            union(to_crawl, links_on_page)
            
            crawled.append(page)

    logging.info(f"Index total size: {len(index)}")
    return index, graph
