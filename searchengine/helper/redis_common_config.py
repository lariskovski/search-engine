import redis

pool = redis.ConnectionPool(host='hostname', port=6379, db=1, decode_responses=True)

redis_conn = redis.Redis(connection_pool=pool)
