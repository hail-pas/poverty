from fastapi import FastAPI, Depends

import settings
from apps.admin.depends import sign_required
from apps.admin.routes import api_router

app = FastAPI(
    title='Poverty运营后台API接口文档',
    openapi_prefix='/admin',
    debug=settings.DEBUG,
)

app.include_router(api_router, dependencies=[Depends(sign_required)])