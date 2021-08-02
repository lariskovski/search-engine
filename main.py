import logging
from searchengine.crawler import crawl_web
from searchengine.searcher import lookup
from searchengine.ranker import compute_ranks

def main():
    # logging.basicConfig(level=logging.INFO)
    
    seed = "https://udacity.github.io/cs101x/urank/" # Couple links example
    # seed = "https://gutenberg.org/cache/epub/1661/pg1661.txt" # A lot of keywords example
    
    index, graph = crawl_web(seed)

    ranks = compute_ranks(graph)
    print(ranks)

    print(lookup(index, 'buttercream'))
    print(lookup(index, 'hummus'))
    print(lookup(index, 'a'))

if __name__ == "__main__":
    main()