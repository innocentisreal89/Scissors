from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

# # Configure the cache
cache = Cache(config={'CACHE_TYPE': 'simple'})  #Set the cache type to 'simple'


# Configure the Redis storage backend
redis_client = Redis(host='localhost', port=6379, db=0)


# limiter = None  # Declare the limiter object outside the function
limiter = Limiter(
                  key_func=get_remote_address,
                  storage_uri="memory://" ,
                #   storage_uri=redis_client,
                  storage_options={"socket_connect_timeout": 30},
                  strategy="fixed-window",  # or "moving-window"
    ) 
BLOCKLIST = set()
