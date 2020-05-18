from arq import cron
from arq.connections import RedisSettings
from tortoise import Tortoise

import settings
from apps.arq import ArqQueue
from paralib.redis import AsyncRedisUtil
from settings import TORTOISE_ORM


async def startup(ctx):
    await Tortoise.init(config=TORTOISE_ORM)
    await AsyncRedisUtil.init(**settings.REDIS)


async def shutdown(ctx):
    await Tortoise.close_connections()
    await AsyncRedisUtil.close()


class NotifyWorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    queue_name = ArqQueue.notify.value
    redis_settings = RedisSettings(**settings.ARQ)
    functions = []


class TaskWorkerSettings:
    redis_settings = RedisSettings(**settings.ARQ)
    functions = []
    on_startup = startup
    on_shutdown = shutdown
    queue_name = ArqQueue.task.value


class TimingWorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    queue_name = ArqQueue.timing.value
    redis_settings = RedisSettings(**settings.ARQ)
    cron_jobs = [
        # cron(timing_notify_ks_task, minute={x for x in range(0, 60, 3)}),
        # cron(download_ks_task, minute={x for x in range(0, 60, 5)}),
        # cron(timing_push_task, minute={x for x in range(0, 60, 5)}),
        # cron(timing_user_rebate, hour=0, minute=20)
    ]
