from fastapi import APIRouter

from apps.admin.routes import login

api_router = APIRouter()

api_router.include_router(login.router, tags=["登录"])
