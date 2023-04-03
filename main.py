from fastapi import FastAPI

from core.configs import settings
from api.api import api


app = FastAPI(title='articles-api')
app.include_router(router=api, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    from dotenv import load_dotenv
    from os import getenv
    import uvicorn
    
    load_dotenv()
    
    PORT = getenv('PORT')
    HOST = getenv('HOST')
    
    uvicorn.run("main:app", host=HOST, port=int(PORT), reload=True, log_level='info')

