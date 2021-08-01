from crawler.utils import timer
import logging

logging.basicConfig(level=logging.INFO)


@timer
def crawl_web(seed):
    ''' Starts crawling pages from the seed using Depth-first Search'''
    from crawler.parser import PageParser, format_content, union
    from crawler.crawler import get_page_content, add_page_to_index, get_all_links

    to_crawl =  [seed]
    crawled = []

    index = {}
    
    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            logging.info(f"Crawling page: {page}")
            content = get_page_content(page)

            # formating content removes html tags
            add_page_to_index(index, page, format_content(PageParser(), content))
            
            links_on_page = get_all_links(content)
            logging.info(f"Links found on page: {links_on_page}")
            union(to_crawl, links_on_page)
            
            crawled.append(page)

    logging.info(f"Index total size: {len(index)}")
    return index


def lookup(index:list, keyword:str) -> list:
    if keyword in index:
        return index[keyword]
    return []


if __name__ == "__main__":
    # seed = "https://udacity.github.io/cs101x/urank/" # Couple links example
    seed = "https://gutenberg.org/cache/epub/1661/pg1661.txt" # A lot of keywords example
    index = crawl_web(seed)
    # print(lookup(index, 'buttercream'))
    # print(lookup(index, 'hummus'))
    # print(lookup(index, 'a'))
