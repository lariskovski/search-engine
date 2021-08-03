import pika, sys, os
import requests
import json
import logging
from dotenv import load_dotenv, find_dotenv

# loggin profile
# logging.basicConfig(level=logging.INFO)

# RabbitMQ config
load_dotenv(find_dotenv())
INDEXER_API_URL =  os.getenv('INDEXER_API_URL')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')
RABBITMQ_INDEX_QUEUE = os.getenv('RABBITMQ_INDEX_QUEUE')


def main():
    # Setup
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST,
                                    5672,
                                    '/',
                                    credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_INDEX_QUEUE)

    def callback(ch, method, properties, body):
        # data to be sent to api
        page, content = json.loads(body)
        data = {'page': page,
                'content': content}
        # sending post request and saving response as response object
        response = requests.post(url=INDEXER_API_URL, data=data)
        print(response.text)
        # logging.info(f"index consumer recieved: {page} {content}")

    # Consuming config
    channel.basic_consume(queue=RABBITMQ_INDEX_QUEUE, on_message_callback=callback, auto_ack=True)
    print('Waiting for messages')
    channel.start_consuming()

if __name__ == "__main__":
    main()