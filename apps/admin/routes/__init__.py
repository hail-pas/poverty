from fastapi import Depends

from . import login, site, rest
from ..paralib import app
from ..paralib.depends import jwt_required

app.include_router(login.router)
app.include_router(site.router)
app.include_router(rest.router, dependencies=[Depends(jwt_required)], prefix='/rest')
