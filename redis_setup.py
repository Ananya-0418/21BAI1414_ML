import redis
import json
import time

class RedisClient:
    def __init__(self, host='localhost', port=6379, decode_responses=True):
        self.client = redis.StrictRedis(host=host, port=port, decode_responses=decode_responses)

# Function to handle rate limiting
def rate_limit(user_id, redis_client):
    key = f"user:{user_id}:requests"
    requests_made = redis_client.get(key)
    
    if requests_made is None:
        redis_client.set(key, 1, ex=3600)  # 1 hour window
        return False
    elif int(requests_made) >= 5:
        return True
    else:
        redis_client.incr(key)
        return False

# Function to cache the response in Redis
def cache_response(query, result, redis_client):
    redis_client.set(query, json.dumps(result), ex=3600)  # Cache for 1 hour

