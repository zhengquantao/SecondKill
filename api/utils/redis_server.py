import redis


def redis_server():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
    conn = redis.Redis(connection_pool=pool)
    return conn
redis_server()