
def crawl_web(seed):
    ''' Starts crawling pages from the seed using Depth-first Search'''
    from helpers.parser import PageParser, format_content
    from helpers.crawler import add_page_to_index, get_all_links
    from helpers.utils import union, get_page_content

    to_crawl =  [seed]
    crawled = []

    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            try:
                content = get_page_content(page)
                '''HTML Formatter removes html tags for better keyword mapping.
                   Passing content instead of the format_content(content) to add_page_to_index
                   would still work but result in poluted index keywords i.e. containing html tags'''
                add_page_to_index(index, page, format_content(PageParser(), content))
                # add_page_to_index(index, page, content)
                union(to_crawl, get_all_links(content))
                crawled.append(page)
            except Exception as e:
                print(f"Couldnt get {page}", e)

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
