import settings
from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI
from paralib.redis import AsyncRedisUtil
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from .api import app as api_app
from .admin import app as admin_app


def init_apps(main_app: Starlette, *sub_apps):
    @main_app.on_event('startup')
    async def init() -> None:
        # 初始化redis
        await AsyncRedisUtil.init(**settings.REDIS)
        # 初始化arq
        arq = await create_pool(RedisSettings(**settings.ARQ))

        for app in [main_app, *sub_apps]:
            app.arq = arq

    @main_app.on_event('shutdown')
    async def close() -> None:
        await AsyncRedisUtil.close()
        main_app.arq.close()


def create_app():
    fast_app = FastAPI(debug=settings.DEBUG)
    fast_app.mount('/api', api_app)
    fast_app.mount('/admin', admin_app)

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    fast_app.add_middleware(SentryAsgiMiddleware)
    init_apps(fast_app, api_app, admin_app)
    return fast_app
