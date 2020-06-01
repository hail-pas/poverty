from arq import ArqRedis

from apps.arq import ArqQueue, ArqTask


async def timing_monitor(ctx):
    redis_pool = ctx['redis']  # type:ArqRedis
    await redis_pool.enqueue_job(ArqTask.monitor.value, _queue_name=ArqQueue.notify.value)


async def monitor(ctx, **kwags):
    pass
