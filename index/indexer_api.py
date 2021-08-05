from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
import logging
import pymongo
import json
import os

logging.basicConfig(level=logging.INFO)

# MongoDB envs
load_dotenv(find_dotenv())
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
MONGODB_CLUSTER    = os.getenv('MONGODB_CLUSTER')
MONGODB_DB_NAME    = os.getenv('MONGODB_DB_NAME')
MONGODB_USER       = os.getenv('MONGODB_USER')
MONGODB_PASS       = os.getenv('MONGODB_PASS')

# MongoDB config
try:
    client     = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER}/")
    db         = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION]
except ServerSelectionTimeoutError as e:
    stderr.write(f"Could not connect to MongoDB: {e}")


def add_to_index(keyword: str, url: str) -> None:
    ''' Populates Mongo collection with a list of urls where a certain keyword appears.

        Adds entry keyword:url if not there
        Appends url to keyword entry already exists.
    '''
    response = collection.find_one({"keyword": keyword}) # if not found -> None
    
    if response == None:
        # Adds new keyword entry to index
        data   = { 'keyword': keyword, 'urls' : [url] }
        result = collection.insert_one(data)
        logging.info(f"Added new entry: id: {result.inserted_id}, keyword: {keyword}, url {url}")
        
    else:
        # Append to existing keyword urls' list
        result = collection.update_one({ "keyword": keyword },
                                       { "$addToSet": { "urls": url } }) # addToSet only adds if entry doesnt exist
        
        # Logging-only logic
        if result.modified_count == 0:
            logging.info(f"Nothing to do. Entry already exists: keyword: {keyword}, url {url}")
        else:
            logging.info(f"RESULT {result.modified_count}")
            logging.info(f"Appended to entry: keyword: {keyword}, url {url}")


def add_page_to_index(url: str, content: str) -> None:
    '''Formats all page content to no-HTML-tags text.
       Calls add_to_index for each word: url mapping'''
    from helper.parser import PageParser

    # Strips HTML structure from content
    parser = PageParser()
    words  = parser.format_content(content).split()

    for word in words:
        add_to_index(word, url)


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/', methods = ['POST'])
    def populate_index():
        data = request.form 
        add_page_to_index(data['page'], data['content'])
        return data

    @app.route('/index', methods = ['GET'])
    def get_index_size():
        index_size = str(collection.count_documents({}))
        return index_size

    @app.route('/url', methods = ['GET'])
    def get_urls_for_keyword():
        # curl localhost:5000/url?keyword=hummus
        keyword = request.args['keyword']
        response = collection.find_one({"keyword": keyword}) # if not found -> None
        if response != None:
            urls = response["urls"]
            data = {
                    "keyword": keyword,
                    "urls": [url for url in urls if len(urls) > 1 ]
                    }
            return json.dumps(data)
        else:
            logging.critical(f"No match found for keyword {keyword}")
            return json.dumps({'message': 'no match'})


    app.run(host="0.0.0.0", port=5000, debug=True)
