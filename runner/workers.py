from arq import cron
from arq.connections import RedisSettings
from tortoise import Tortoise

import settings
from apps.api.jobs import timing_monitor
from apps.arq import ArqQueue
from paralib.redis import AsyncRedisUtil
from settings import TORTOISE_ORM


async def startup(ctx):
    await Tortoise.init(config=TORTOISE_ORM)
    await AsyncRedisUtil.init(**settings.REDIS)


async def shutdown(ctx):
    await Tortoise.close_connections()
    await AsyncRedisUtil.close()


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
        cron(timing_monitor, hour=0, minute=0),
        # cron(timing_, minute={x for x in range(0, 60, 3)})
    ]
