from dotenv import load_dotenv, find_dotenv
import pika, sys, os
import requests
import logging
import json


logging.basicConfig(level=logging.INFO)

# RabbitMQ config
load_dotenv(find_dotenv())
RABBITMQ_INDEX_QUEUE = os.getenv('RABBITMQ_INDEX_QUEUE')
INDEXER_API_URL      = os.getenv('INDEXER_API_URL')
RABBITMQ_HOST        = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER        = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS        = os.getenv('RABBITMQ_PASS')


def callback(ch, method, properties, body):
    '''Defines how messages are gonna be treated as they are being consumed.
       Fetches page and content values from body.
       Sends them via POST request to Indexer API.
    '''
    # Fetches data to be sent to API
    page, content = json.loads(body)

    data = {
             'page': page,
             'content': content
           }

    # Sends POST request to Indexer API
    response = requests.post(url=INDEXER_API_URL,
                             data=data)
    # Logs Indexer API response
    logging.info(response.text)


def main():
    # RabbitMQ setup
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters  = pika.ConnectionParameters(RABBITMQ_HOST,
                                           5672,
                                           '/',
                                           credentials)

    connection  = pika.BlockingConnection(parameters)
    channel     = connection.channel()

    channel.queue_declare(queue=RABBITMQ_INDEX_QUEUE)

    # Queue consuming config
    channel.basic_consume(queue=RABBITMQ_INDEX_QUEUE,
                          on_message_callback=callback,
                          auto_ack=True)

    logging.info('Waiting for messages')
    channel.start_consuming()


if __name__ == "__main__":
    main()
