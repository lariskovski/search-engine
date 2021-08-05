from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
import requests, json
import os, time
import logging

# API calls envs
load_dotenv(find_dotenv())
INDEX_API = os.getenv('INDEX_API')
RANK_API  = os.getenv('RANK_API')

logging.basicConfig(level=logging.INFO)


def lookup(keyword:str) -> dict:
    ''' Asks Index API for the urls of keyword, returns entry if exists otherwise, None'''
    retry_api_connection = True
    while retry_api_connection:
        try:
            request = requests.get(INDEX_API + "/url", params={ 'keyword': keyword })
            response  = json.loads(request.text)
            logging.debug(f"Successfully connected to {INDEX_API}")
            retry_api_connection = False

        except Exception as e:
            logging.critical(f"Could not connect to {INDEX_API} - {e}")
            logging.info(f"Retrying connection to {INDEX_API}")
            time.sleep(1)

    keyword, urls = response['keyword'], response['urls']
    logging.debug(f"Found urls for {keyword}: {urls}")
    return urls


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
                    request   = requests.get(RANK_API + "/rank", params={ 'page': url })
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
        best_ranked_url    = sorted_ranked_urls.popitem()[0] # pop returns a list [ url, rank ]

        return best_ranked_url

    else:
        return ''


if __name__ == "__main__":
    
    app = Flask(__name__)

    @app.route('/search', methods = ['GET'])
    def get_best_url():
        # curl localhost:6000/search?keyword=hummus
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
