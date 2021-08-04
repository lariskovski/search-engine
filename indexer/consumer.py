from dotenv import load_dotenv, find_dotenv
import pika, sys, os
import requests
import logging
import json
import time

logging.basicConfig(level=logging.INFO)

# RabbitMQ config
load_dotenv(find_dotenv())
INDEXER_API_URL = os.getenv('INDEXER_API_URL')
RABBITMQ_QUEUE  = os.getenv('RABBITMQ_QUEUE')
RABBITMQ_HOST   = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER   = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS   = os.getenv('RABBITMQ_PASS')


def callback(channel, method, properties, body):
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

    try:
        # Sends POST request to Indexer API
        response = requests.post(url=INDEXER_API_URL,
                                 data=data,
                                 timeout=5)
        logging.info(f"Successfully connected: {INDEXER_API_URL}")
        # Logs Indexer API response
        logging.info(response.text)

    except requests.exceptions.RequestException as e: # General Exception Handle
        logging.info(f"Error reaching {INDEXER_API_URL}. Retry in a few seconds.")
        time.sleep(5) # Prevents loop
        logging.info(f"Resending message to queue. page: {page}")
        # Resends failed-to-be-delivered message to queue
        channel.basic_publish(exchange='',
                              routing_key=RABBITMQ_QUEUE,
                              body=json.dumps([page, content]))


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

    logging.info('Successfully connected to broker. Waiting for messages')
    channel.start_consuming()


if __name__ == "__main__":
    main()
