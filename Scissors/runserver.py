from Scissors import create_app
from config.config import config_dict 


app =create_app(config=config_dict['prod']) 

app =create_app() 
if __name__== '__main__':
    app.run()
   