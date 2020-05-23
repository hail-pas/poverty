import asyncio
from datetime import datetime

from fastapi import APIRouter
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse

from apps.admin.paralib.common import pwd_context
from apps.web.common import send_html
from db.models import Admin
from settings import templates

router = APIRouter()


@router.get(
    "/upload",
    description="文件上传"
)
async def upload_page(request: Request):
    return templates.TemplateResponse("web/upload_file.html", {"request": request})


@router.post(
    "/xls/2/html",
    description="xls处理成HTML文档"
)
async def xls2html(request: Request, back_ground_tasks: BackgroundTasks):
    form_data = await request.form()
    file = form_data.get("file").file._file
    if not file.getvalue():
        return templates.TemplateResponse("web/failure.html",
                                          {"request": request, "message": "没有文件上传！"})
    back_ground_tasks.add_task(send_html, file)
    return templates.TemplateResponse("web/success.html",
                                      {"request": request, "email_address": "hypofiasco@outlook.com"})
