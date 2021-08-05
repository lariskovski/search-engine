from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
import logging
import json
import redis
import os

logging.basicConfig(level=logging.INFO)

# Redis envs
load_dotenv(find_dotenv())
REDIS_HASH_NAME = os.getenv('REDIS_HASH_NAME')
REDIS_HOST      = os.getenv('REDIS_HOST')

# Redis connection with retries
retry_connection = True
while retry_connection:
    try:
        pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
        rank = redis.Redis(connection_pool=pool)
        retry_connection = False

    except Exception as e:
        logging.error(e)
        logging.info("Retrying connection to Redis in 1 second.")
        sleep(1)


if __name__ == "__main__":
    
    app = Flask(__name__)

    @app.route('/rank', methods = ['GET'])
    def get_page_rank():
        # curl localhost:5000/rank?page=https://udacity.github.io/cs101x/urank/nickel.html
        page = request.args['page']
        data = {
                "page": page,
                "rank": rank.hget(REDIS_HASH_NAME, page)
                }
        return json.dumps(data)

    app.run(host="0.0.0.0", port=5000, debug=True)
