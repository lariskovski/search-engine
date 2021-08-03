from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
import logging
import pymongo
import json
import os


# RabbitMQ envs
load_dotenv(find_dotenv())
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
MONGODB_CLUSTER    = os.getenv('MONGODB_CLUSTER')
MONGODB_DB_NAME    = os.getenv('MONGODB_DB_NAME')
MONGODB_USER       = os.getenv('MONGODB_USER')
MONGODB_PASS       = os.getenv('MONGODB_PASS')


# RabbitMQ configs
try:
    client     = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER}/")
    db         = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION]
    print('Successfully set up a database handle')
except ServerSelectionTimeoutError as e:
    stderr.write(f"Could not connect to MongoDB: {e}")


def add_to_index(keyword: str, url: str) -> None:
    ''' Adds keyword and correspondent url to index hashtable if its not there'''

    response = collection.find_one({"keyword": keyword}) # if not found -> None
    
    if response == None:
        data   = {'keyword' : keyword, 'urls' : [u for u in url] }
        result = collection.insert_one(data)
        # return {result.inserted_id}
    else:
        # addToSet only adds if it doesnt exist
        result = collection.update_one({"keyword": keyword}, {"$addToSet": {"urls": url}})


def add_page_to_index(url: str, content: str) -> None:
    from helper.parser import PageParser
    '''Formats all page content to no-HTML-tags text and passes each word into add_to_index()'''

    parser = PageParser()
    words  = parser.format_content(content).split()

    for word in words:
        add_to_index(word, url)
    # return index


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/', methods = ['POST'])
    def populate_index():
        data    = request.form 
        add_page_to_index(data['page'],  data['content'])
        return data

    @app.route('/index', methods = ['GET'])
    def get_index_size():
        return str(collection.count_documents({}))
    
    app.run(host="0.0.0.0", port=5000, debug=True)
