from dotenv import load_dotenv, find_dotenv
import logging
import pymongo
import os

# MongoDB envs
load_dotenv(find_dotenv())
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
MONGODB_CLUSTER    = os.getenv('MONGODB_CLUSTER')
MONGODB_DB_NAME    = os.getenv('MONGODB_DB_NAME')
MONGODB_USER       = os.getenv('MONGODB_USER')
MONGODB_PASS       = os.getenv('MONGODB_PASS')

logging.basicConfig(level=logging.INFO)

# MongoDB config
try:
    client     = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER}/")
    db         = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION]

except ServerSelectionTimeoutError as e:
    stderr.write(f"Could not connect to MongoDB: {e}")


def lookup(keyword:str) -> dict:
    ''' Looks for keyword on indexer collection, returns entry if exists otherwise, None'''
    response = collection.find_one({"keyword": keyword}) # if not found -> None
    if response == None:
        logging.info(f"Not found index entry: {keyword}")
        return None
    else:
        logging.info(f"Found entry: {response}")
        return response['urls']


def lookup_best(index: dict, keyword: str, ranks: dict) -> str:
    urls_for_kw: list = lookup(index, keyword)

    if urls_for_kw:
        # Get set intersection between all possible urls for a given keyword and the ranked dictionary
        url_rank_intersection: set = set(urls_for_kw).intersection(set(ranks.keys()))
        # transforms set into a dict for later sorting
        selected_ranks: dict = {key : ranks[key] for key in url_rank_intersection}
        # sorts values in reverse order. gets most popular page
        sort_selected_rank:list = [k for k, v in sorted(selected_ranks.items(), key=lambda item: item[1], reverse=True)]

        best_url = sort_selected_rank[0]
        
        return best_url
    
    return None

if __name__ == "__main__":
    s1 = lookup("hummus")
    s2 = lookup("notfound")
    # print(s1)
    # print(s2)