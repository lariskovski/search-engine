import redis
pool = redis.ConnectionPool(host='147.182.230.208', port=6379, db=0, decode_responses=True)
graph_hashtable = redis.Redis(connection_pool=pool)


def str_to_list(string):
    string = string.replace('[', '').replace(']', '').replace("'", '')
    return string.split(',')

def format_redis_dict(dictionary):
    for k, v in dictionary.items():
        dictionary[k] = str_to_list(v)
    return dictionary