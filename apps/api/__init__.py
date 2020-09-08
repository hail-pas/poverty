import settings
from fastapi import FastAPI, Depends

from apps.api.depends import sign_required
from apps.api.routes import api_router
from apps.response import AesResponse

app = FastAPI(
    title='Poverty API接口文档',
    root_path='/api',
    debug=settings.DEBUG,
    default_response_class=AesResponse
)
app.include_router(api_router, dependencies=[Depends(sign_required)])
