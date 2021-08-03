import pika, sys, os
import requests
import json

def main():
    QUEUE = "add_to_index"
    credentials = pika.PlainCredentials('user', 'bitnami')
    parameters = pika.ConnectionParameters('do.larissa.tech',
                                    5672,
                                    '/',
                                    credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)

    def callback(ch, method, properties, body):
        # MAKES CALL TO INDEXER API
        # posting page and content
        body = json.loads(body)
        # LOGGS EACH ENTRY
        print(f"Received {body}")

    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()