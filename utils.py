from redis import redis_client

def convert_objectid_to_str(document):
    if isinstance(document, dict):
        document['_id'] = str(document['_id'])
    return document

def rate_limit(user_id):
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
