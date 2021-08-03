from dotenv import load_dotenv, find_dotenv
import pika, sys, os
import requests
import logging
import json
import os


load_dotenv(find_dotenv())
INDEXER_API_URL =  os.getenv('INDEXER_API_URL')
RABBITMQ_GRAPH_QUEUE = os.getenv('RABBITMQ_GRAPH_QUEUE')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')


def main():
    # Setup
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST,
                                    5672,
                                    '/',
                                    credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_GRAPH_QUEUE)

    def callback(ch, method, properties, body):
        # data to be sent to api
        message = json.loads(body)
        # send infos to redis
        print(message)

    channel.basic_consume(queue=RABBITMQ_GRAPH_QUEUE, on_message_callback=callback, auto_ack=True)

    print('Waiting for messages')
    channel.start_consuming()

if __name__ == "__main__":
    main()