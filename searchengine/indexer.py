from flask import Flask, request
import logging
import redis
import os

from dotenv import load_dotenv, find_dotenv

# REDIS envs
load_dotenv(find_dotenv())
REDIS_HOST =  os.getenv('REDIS_HOST')

pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=1, decode_responses=True)
index = redis.Redis(connection_pool=pool)

def add_to_index(index: dict, keyword: str, url: str) -> None:
    from helper.utils import str_to_list
    '''Adds keyword and correspondent url to index hashtable'''
    # Check if keyword is already in index
    result = index.hget("index", keyword)
    if result == None:
        # Add new entry to index
        index.hset("index", keyword, url)
        # logging.info(f"New keyword: {keyword}")
    else:
        # Update keyword urls list
        updated_url_list = str_to_list(result).append(url)
        formatted_list_into_str = str(updated_url_list)
        index.hset("index", keyword, formatted_list_into_str)


def add_page_to_index(index: list, url: str, content: str) -> dict:
    from helper.parser import PageParser
    '''Formats all page content to no-HTML-tags text and passes each word into add_to_index()'''
    parser = PageParser()
    words = parser.format_content(content).split()
    for word in words:
        add_to_index(index, word, url)
    return index


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/', methods = ['POST'])
    def populate_index():
        data = request.form 
        page = data['page']
        content = data['content']
        add_page_to_index(index, page, content)
        return data

    @app.route('/index', methods = ['GET'])
    def get_index():
        return index.hgetall('index')
    app.run(host="0.0.0.0", port=5000, debug=True)
