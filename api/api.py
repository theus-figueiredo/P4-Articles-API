from fastapi import APIRouter
from api.routes.articles_routes import article_route
from api.routes.user_routes import user_router

api = APIRouter()

api.include_router(router=article_route, prefix='/articles', tags=['article'])
api.include_router(router=user_router, prefix='users', tags=['user'])
