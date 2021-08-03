from crawler_helper.timer import timer
from dotenv import load_dotenv, find_dotenv
import logging
import json
import pika
import os

# RabbitMQ envs
load_dotenv(find_dotenv())
RABBITMQ_INDEX_QUEUE =  os.getenv('RABBITMQ_INDEX_QUEUE')
RABBITMQ_GRAPH_QUEUE =  os.getenv('RABBITMQ_GRAPH_QUEUE')
RABBITMQ_HOST        = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER        = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS        = os.getenv('RABBITMQ_PASS')

# RabbitMQ setup
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters  = pika.ConnectionParameters(RABBITMQ_HOST, 5672, '/', credentials)
connection  = pika.BlockingConnection(parameters)
channel     = connection.channel()


logging.basicConfig(level=logging.INFO)

def publish_to_queue(channel: str, queue: str, message: list) -> None:
    '''Publishes message on given channel/queue'''
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=json.dumps(message))


@timer
def crawl_web(seed: str) -> None:
    from crawler_helper.utils import get_all_links, get_next_target, get_page_content, union
    ''' Starts crawling pages from the given seed using Depth-first Search.
        It's the starting point for the Search Engine System assyncronously feeding the indexer and graphthrough queues.
    '''

    to_crawl =  [seed]
    crawled  = []

    while to_crawl:

        page = to_crawl.pop()
        
        if page not in crawled:

            logging.info(f"Crawling page: {page}")
            content = get_page_content(page)

            # Index Queue
            publish_to_queue(channel, RABBITMQ_INDEX_QUEUE, [page, content])

            links_on_page = get_all_links(content)
            logging.info(f"Links found on page: {links_on_page}")

            # Graph Queue
            publish_to_queue(channel, RABBITMQ_GRAPH_QUEUE, [page, links_on_page])

            union(to_crawl, links_on_page)
            crawled.append(page)


if __name__ == "__main__":
    # seed = "https://gutenberg.org/cache/epub/1661/pg1661.txt"
    seed = "https://udacity.github.io/cs101x/urank/"
    crawl_web(seed)