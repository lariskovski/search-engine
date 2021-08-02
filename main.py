from searchengine.crawler import crawl_web
from searchengine.searcher import lookup, lookup_best
from searchengine.ranker import compute_ranks

def main():
    seed = "https://udacity.github.io/cs101x/urank/" # Couple links example
    # seed = "https://gutenberg.org/cache/epub/1661/pg1661.txt" # A lot of keywords example
    
    index, graph = crawl_web(seed)

    ranks = compute_ranks(graph)
    # prints unordered url ranking
    print(ranks)

    # Get all url for keyword
    # print(lookup(index, 'buttercream'))
    # print(lookup(index, 'the'))
    # print(lookup(index, 'a'))

    # Get best ranked url for keyword
    print(lookup_best(index, 'buttercream', ranks))
    print(lookup_best(index, 'the', ranks))
    print(lookup_best(index, 'a', ranks))

if __name__ == "__main__":
    main()