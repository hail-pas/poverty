from fastapi import APIRouter

from apps.web.routes import docer

web_router = APIRouter()

web_router.include_router(docer.router, prefix="/doc", tags=["文档处理"])
