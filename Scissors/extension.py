from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis


cache = Cache()

# Configure the Redis storage backend
# redis_client = Redis(host='localhost', port=6379, db=0)
limiter = Limiter(key_func=get_remote_address)

#   To handle our login out function 
BLOCKLIST = set()