from crawler.utils import union, get_page_content, timer
import logging


logging.basicConfig(level=logging.INFO)


@timer
def crawl_web(seed):
    ''' Starts crawling pages from the seed using Depth-first Search'''
    from crawler.parser import PageParser, format_content
    from crawler.crawler import add_page_to_index, get_all_links

    to_crawl =  [seed]
    crawled = []

    while to_crawl:
        page = to_crawl.pop()
        logging.info(f"Crawling page: {page}")
        if page not in crawled:
            content = get_page_content(page)
            '''HTML Formatter removes html tags for better keyword mapping.
                Passing content instead of the format_content(content) to add_page_to_index
                would still work but result in poluted index keywords i.e. containing html tags'''
            add_page_to_index(index, page, format_content(PageParser(), content))
            links_on_page = get_all_links(content)
            logging.info(f"Links found on page: {links_on_page}")
            union(to_crawl, links_on_page)
            crawled.append(page)

    return crawled


def lookup(index:list,keyword:str) -> list:
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []


if __name__ == "__main__":
    seed = "https://udacity.github.io/cs101x/urank/"
    index = []
    crawl_web(seed)
    # print(index)
    # print(len(index))
    # for entry in index:
    #     print(entry)
    #     print(entry[0])
    print(lookup(index, 'buttercream'))
    print(lookup(index, 'hummus'))
    print(lookup(index, 'a'))
