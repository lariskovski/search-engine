import logging
from searchengine.crawler import crawl_web
from searchengine.searcher import lookup

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed = "https://udacity.github.io/cs101x/urank/" # Couple links example
    # seed = "https://gutenberg.org/cache/epub/1661/pg1661.txt" # A lot of keywords example
    index = crawl_web(seed)
    print(lookup(index, 'buttercream'))
    print(lookup(index, 'hummus'))
    print(lookup(index, 'a'))
