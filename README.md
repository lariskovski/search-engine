# Search Engine

The project gets on how search engines work by building on from scratch in learning Python while having fun.
Based on [Udacity Intro to Computer Science](https://classroom.udacity.com/courses/cs101) course.

## Requirements

- Python >= 3.8

## Course Main Topics

    - Variables
    - Basic Operations and Conditionals
    - Defining functions and Python built-in functions
    - Strings, Lists, Dictionaries
    - Creating Hashtables
    - For loops, While loops
    - Time Complexity on lists vs hashtables and improving performance
    - How to implement Recursion
    - Fibonacci and Palindromes with and without recursion
    - What are Graphs and how to use them in Python
    - Ranking pages algorithms and a (not so) simple implementation
    - Searching through hashtables and ranks for the better results

### Few Extras:

    - timer Decorator
    - Stripping HTML from string

## The Search Engine

As this project does not aim to be a full-blown Google-like engine, it uses a controlled environment with two main seeds provided by the course intructors. Each seed is better for a certain feature example.

- https://udacity.github.io/cs101x/urank/: Few linked web pages and few keywords about recepies
- https://gutenberg.org/cache/epub/1661/pg1661.txt: A book page with +1500 keywords and not links

The first one makes very clear how the engine's crawler goes from one page to another.
While the second is better at showing how the engine indexes new keywords.
Both are pretty good exemplifing the searches.

## Running Locally

### App

~~~~
pipenv shell
pipenv install
~~~~

### Redis
~~~~
# Redis
# port TCP	5672
mkdir redis ; cd redis
wget https://raw.githubusercontent.com/antirez/redis/4.0/redis.conf
sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g'  redis.conf
chmod 644 redis.conf
docker network create search-engine
docker run --rm -d \
    --network search-engine \
    -v $(pwd)/redis.conf:/etc/redis.conf \
    -p 6379:6379 \
    redis:6.2-alpine redis-server /etc/redis.conf
# Check the hashtable on the container
redis-cli
hgetall graph
~~~~

test.py
~~~~
import redis
pool = redis.ConnectionPool(host='hostname', port=6379, db=1, decode_responses=True)
hashtable = redis.Redis(connection_pool=pool)

hashtable.hset("index", "keyword1", "value1")
~~~~

### RabbitMQ

~~~~
# RabbitMQ
# Ports TCP	5672, 15672
docker run -d \
    -e RABBITMQ_SECURE_PASSWORD=yes \
    -p 5672:5672 \
    -p 15672:15672 \
    --restart=always \
    --hostname rabbitmq-master \
    docker.io/bitnami/rabbitmq:3.8
# Acess http://hostname:15672/
# user/bitnami
~~~~

test.py
~~~~
import pika


credentials = pika.PlainCredentials('user', 'pass')
parameters = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='hello')


channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")

connection.close()
~~~~

# Testing Endpoints

~~~~
# Flask post
curl -X POST localhost:5000 -d "param1=value1&param2=this is value2"
~~~~

## Sources

[Web Crawling vs Web Scraping](https://blog.apify.com/what-is-web-scraping/)

[Documenting Python Code](https://realpython.com/documenting-python-code/)

[Python dotenv](https://www.nylas.com/blog/making-use-of-environment-variables-in-python/)