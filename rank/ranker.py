from dotenv import load_dotenv, find_dotenv
from time import sleep
import logging
import pymongo
import redis
import os

logging.basicConfig(level=logging.INFO)

# MongoDB envs
load_dotenv(find_dotenv())
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
MONGODB_CLUSTER    = os.getenv('MONGODB_CLUSTER')
MONGODB_DB_NAME    = os.getenv('MONGODB_DB_NAME')
MONGODB_USER       = os.getenv('MONGODB_USER')
MONGODB_PASS       = os.getenv('MONGODB_PASS')

REDIS_HASH_NAME    = os.getenv('REDIS_HASH_NAME')
REDIS_HOST         = os.getenv('REDIS_HOST')

# Redis connection with retries
retry_connection = True
while retry_connection:
    try:
        pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
        hashtable = redis.Redis(connection_pool=pool)
        retry_connection = False

    except redis.exceptions.ConnectionError as e:
        logging.error(e)
        logging.info("Retrying connection to Redis in 1 second.")
        sleep(1)


def get_all_graphs()-> dict:
    '''Get all graphs from collection'''

    # MongoDB config
    try:
        client     = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER}/")
        db         = client[MONGODB_DB_NAME]
        collection = db[MONGODB_COLLECTION]
    except ServerSelectionTimeoutError as e:
        stderr.write(f"Could not connect to MongoDB: {e}")
    
    cursor =  collection.find({})
    graph = {k["page"]:k["urls"] for k in cursor}
    # Drops Collection
    # collection.drop()
    return graph


def compute_ranks() -> None:
    '''
        Ranks pages present on graphs collection (page:urls).
        Ranking logic is: The most pointed at page is the most popular/best ranked.
    '''
    DAMPING_FACTOR: float = 0.8
    RANK_ACCURACY: int = 10
    
    graph = get_all_graphs()

    ranks: dict = {}
    total_pages_number: int = len(graph)
    
    for page in graph:
        # initializes ranks
        ranks[page] = 1.0 / total_pages_number

    for _ in range(RANK_ACCURACY):
        new_ranks: dict = {}
        for page in graph:
            new_rank: float = (1 - DAMPING_FACTOR) / total_pages_number

            for node in graph:
                # this loop looks for a page in all the graph's nodes
                # each time it finds the page in a node, means its refered to
                # so we increase its popularity record
                if page in graph[node]:
                    # pages current popularity / all links on the page
                    # which means if the page has a lot of links in it, decreases popularity
                    # https://classroom.udacity.com/courses/cs101/lessons/48756019/concepts/484202570923
                    new_rank += DAMPING_FACTOR * (ranks[node] /len(graph[node]))

            # Set new rank on Redis
            hashtable.hset(REDIS_HASH_NAME, page, new_rank)
            logging.info(f"Successfully added page rank: {page}: {new_rank}")


if __name__ == "__main__":
    compute_ranks()