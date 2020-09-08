from fastapi import APIRouter

from apps.web.routes import docer, qrcode

web_router = APIRouter()

web_router.include_router(docer.router, prefix="/doc", tags=["文档处理"])
web_router.include_router(qrcode.router, prefix="/qr-code", tags=["二维码"])
