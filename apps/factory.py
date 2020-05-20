import settings
from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI
from paralib.redis import AsyncRedisUtil
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.starlette import register_tortoise
from .api import app as api_app
from .admin import app as admin_app, site
from .web import app as web_app


def init_apps(main_app: Starlette, *sub_apps):
    @main_app.on_event('startup')
    async def init() -> None:
        # 初始化redis
        await AsyncRedisUtil.init(**settings.REDIS)
        # 初始化arq
        arq = await create_pool(RedisSettings(**settings.ARQ))
        #
        # 初始化admin_app
        admin_app.init(
            user_model='Admin',
            admin_secret=settings.ADMIN_SECRET,
            tortoise_app='models',
            site=site
        )

        for app in [main_app, *sub_apps]:
            app.arq = arq

    @main_app.on_event('shutdown')
    async def close() -> None:
        await AsyncRedisUtil.close()
        main_app.arq.close()


def create_app():
    fast_app = FastAPI(debug=settings.DEBUG)
    fast_app.mount("/static", StaticFiles(directory="static"), name="static")
    fast_app.mount('/api', api_app)
    fast_app.mount('/admin', admin_app)
    fast_app.mount('/web', web_app)

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    fast_app.add_middleware(SentryAsgiMiddleware)
    register_tortoise(fast_app, config=settings.TORTOISE_ORM)
    init_apps(fast_app, api_app, admin_app, web_app)
    return fast_app
