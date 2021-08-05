from dotenv import load_dotenv, find_dotenv
import requests, json
import os, time
import logging
import pymongo

# MongoDB envs
load_dotenv(find_dotenv())
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
MONGODB_CLUSTER    = os.getenv('MONGODB_CLUSTER')
MONGODB_DB_NAME    = os.getenv('MONGODB_DB_NAME')
MONGODB_USER       = os.getenv('MONGODB_USER')
MONGODB_PASS       = os.getenv('MONGODB_PASS')

RANK_API           =os.getenv('RANK_API')

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


def lookup_best(keyword: str) -> str:
    ''' All possible urls for given keyword from lookup [url1, url2, url3]'''
    urls_for_kw: list = lookup(keyword)

    unsorted_ranked_urls = {}

    # Get each url's rank from Rank API
    for url in urls_for_kw:
        # Connection to Rank API. Retries if any exception is thrown
        retry_api_connection = True
        while retry_api_connection:
            try:
                request = requests.get(RANK_API + "/rank", params={ 'page': url })
                response  = json.loads(request.text)
                logging.debug(f"Successfully connected to {RANK_API}")
                retry_api_connection = False

            except Exception as e:
                logging.critical(f"Could not connect to {RANK_API} - {e}")
                logging.info(f"Retrying connection to {RANK_API}")
                time.sleep(1)

        # Adds entry {url: rank} to unsorted dict
        url, rank = response['page'], response['rank']
        unsorted_ranked_urls[url] = rank
        logging.debug(f"Found rank for {url}: {rank}")
    
    # Sorts and returns best ranked page for the provided keyword
    sorted_ranked_urls = {k: v for k, v in sorted(unsorted_ranked_urls.items(), key=lambda item: item[1])}
    best_ranked        = sorted_ranked_urls.popitem()

    return best_ranked

if __name__ == "__main__":
    print(lookup_best("hummus"))