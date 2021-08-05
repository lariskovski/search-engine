from dotenv import load_dotenv, find_dotenv
import pika, sys, os
import pymongo
import requests
import logging
import json


logging.basicConfig(level=logging.INFO)

# RabbitMQ env
load_dotenv(find_dotenv())
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
RABBITMQ_HOST  = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER  = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS  = os.getenv('RABBITMQ_PASS')

# MongoDB env
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
MONGODB_CLUSTER    = os.getenv('MONGODB_CLUSTER')
MONGODB_DB_NAME    = os.getenv('MONGODB_DB_NAME')
MONGODB_USER       = os.getenv('MONGODB_USER')
MONGODB_PASS       = os.getenv('MONGODB_PASS')

# MongoDB configs
try:
    client     = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER}/")
    db         = client[MONGODB_DB_NAME]
    collection = db['graph']
except ServerSelectionTimeoutError as e:
    stderr.write(f"Could not connect to MongoDB: {e}")


def callback(ch, method, properties, body):
    '''Defines how messages are gonna be treated as they are being consumed.
       Fetches page and url values from body.
       Sends them to MongoDB graph collection.
    '''
    # Fetches data to be sent to API
    page, urls = json.loads(body)
    data = {
             'page': page,
             'urls' : [url for url in urls]
           }
    # Creates MongoDB document
    result = collection.insert_one(data)
    # Logs in format: {'page': 'x', 'urls': ['y], '_id': ObjectId('1234')}
    logging.info(f"Added entry: {data}")


def main():
    # RabbitMQ setup
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters  = pika.ConnectionParameters(RABBITMQ_HOST,
                                            5672,
                                            '/',
                                            credentials)

    connection  = pika.BlockingConnection(parameters)
    channel     = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE)

    # Queue consuming config
    channel.basic_consume(queue=RABBITMQ_QUEUE,
                          on_message_callback=callback,
                          auto_ack=True)

    logging.info('Waiting for messages')
    channel.start_consuming()


if __name__ == "__main__":
    main()
