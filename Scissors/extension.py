from flask_caching import Cache
# from flask_caching.backends import SimpleCache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
# from app import create_app

# app =create_app() 

# # Configure the cache
cache = Cache(config={'CACHE_TYPE': 'simple'})  #Set the cache type to 'simple'

# cache = SimpleCache()

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

# def configure_limiter(app):
#     from flask_limiter import Limiter
#     from flask_limiter.util import get_remote_address
#     global limiter  # Use the global keyword to access the outer limiter object
    
#     limiter = Limiter(app,
#                   key_func=get_remote_address, 
#                   storage_uri="redis://localhost:6379",
#                   storage_options={"socket_connect_timeout": 30},
#                   strategy="fixed-window",  # or "moving-window"
#     )
#     # Set rate limits for specific routes or globally
#     limiter.limit("10/minute")(app)
    




#   To handle our login out function 
BLOCKLIST = set()
