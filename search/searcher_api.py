from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
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
    
    if urls_for_kw != None:
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
        sorted_ranked_urls   = {k: v for k, v in sorted(unsorted_ranked_urls.items(), key=lambda item: item[1])}
        best_ranked_url = sorted_ranked_urls.popitem()[0] # pop returns a list [ url, rank ]

        return best_ranked_url

    else:
        return ''


if __name__ == "__main__":
    
    app = Flask(__name__)

    @app.route('/search', methods = ['GET'])
    def get_best_url():
        # curl localhost:5000/?keyword=hummus
        keyword = request.args['keyword']
        best_url = lookup_best(keyword)
        if best_url != '':
            data = {
                    "keyword": keyword,
                    "best_ranked_url": best_url
                    }
            return json.dumps(data)
        else:
            return json.dumps({"message": f"No match for keyword {keyword}"})

    app.run(host="0.0.0.0", port=6000, debug=True)
