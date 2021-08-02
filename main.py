from searchengine.crawler import crawl_web
from searchengine.searcher import lookup, lookup_best
from searchengine.ranker import compute_ranks

import redis
pool = redis.ConnectionPool(host='147.182.230.208', port=6379, db=0, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def str_to_list(string):
    string = string.replace('[', '').replace(']', '').replace("'", '')
    return string.split(',')

def format_redis_dict(dictionary):
    for k, v in dictionary.items():
        dictionary[k] = str_to_list(v)
    return dictionary


# print(format_redis_dict(r.hgetall('graph')))


def main():
    seed = "https://udacity.github.io/cs101x/urank/" # Couple links example
    # seed = "https://gutenberg.org/cache/epub/1661/pg1661.txt" # A lot of keywords example
    
    index = crawl_web(seed)

    graph = format_redis_dict(r.hgetall('graph'))
    
    ranks = compute_ranks(graph)
    # prints unordered url ranking
    print(ranks)

    # Get all url for keyword
    # print(lookup(index, 'buttercream'))
    # print(lookup(index, 'the'))
    # print(lookup(index, 'a'))

    # Get best ranked url for keyword
    # print(lookup_best(index, 'buttercream', ranks))
    # print(lookup_best(index, 'olimpíadas', ranks))
    print(lookup_best(index, 'a', ranks))

if __name__ == "__main__":
    main()