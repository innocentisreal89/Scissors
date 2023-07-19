from api import create_app
from .api.config.config import config_dict 


app =create_app(config=config_dict['prod']) 

# app =create_app() # un comment if running dev or test
if __name__== '__main__':
    app.run()
   