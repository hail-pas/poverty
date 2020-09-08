import settings
from fastapi import FastAPI
from apps.web.routes import web_router

app = FastAPI(
    title='Poverty Web接口文档',
    root_path='/web',
    debug=settings.DEBUG,
)
app.include_router(web_router)
