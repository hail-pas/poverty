from fastapi import Depends

import settings
from apps.depends import SignChecker, JwtAuth

sign_required = SignChecker(settings.ADMIN_SECRET)
jwt_required = JwtAuth(settings.ADMIN_SECRET)


async def get_current_admin():
    pass


async def get_client_app(app=Depends(sign_required)):
    return app
