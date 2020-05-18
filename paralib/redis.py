import aioredis
import redis
from aioredis import Redis
from redis import WatchError


class AsyncRedisUtil:
    """
    异步redis操作
    """

    r = None  # type:Redis

    @classmethod
    async def init(cls, host='127.0.0.1', port=6379, password=None, db=0, **kwargs):
        cls.r = await aioredis.create_redis_pool(f'redis://{host}:{port}', password=password, db=db, **kwargs)
        return cls.r

    @classmethod
    async def _exp_of_none(cls, *args, exp_of_none, callback):
        if not exp_of_none:
            return await getattr(cls.r, callback)(*args)
        key = args[0]
        tr = cls.r.multi_exec()
        fun = getattr(tr, callback)
        exists = await cls.r.exists(key)
        if not exists:
            fun(*args)
            tr.expire(key, exp_of_none)
            ret, _ = await tr.execute()
        else:
            fun(*args)
            ret = (await tr.execute())[0]
        return ret

    @classmethod
    async def set(cls, key, value, exp=None):
        assert cls.r, 'must call init first'
        await cls.r.set(key, value, expire=exp)

    @classmethod
    async def get(cls, key, default=None):
        assert cls.r, 'must call init first'
        value = await cls.r.get(key)
        if value is None:
            return default
        return value

    @classmethod
    async def hget(cls, name, key, default=0):
        """
        缓存清除，接收list or str
        """
        assert cls.r, 'must call init first'
        v = await cls.r.hget(name, key)
        if v is None:
            return default
        return v

    @classmethod
    async def get_or_set(cls, key, default=None, value_fun=None):
        """
        获取或者设置缓存
        """
        assert cls.r, 'must call init first'
        value = await cls.r.get(key)
        if value is None and default:
            return default
        if value is not None:
            return value
        if value_fun:
            value, exp = await value_fun()
            await cls.r.set(key, value, expire=exp)
        return value

    @classmethod
    async def delete(cls, key):
        """
        缓存清除，接收list or str
        """
        assert cls.r, 'must call init first'
        return await cls.r.delete(key)

    @classmethod
    async def sadd(cls, name, values, exp_of_none=None):
        assert cls.r, 'must call init first'
        return await cls._exp_of_none(name, values, exp_of_none=exp_of_none, callback='sadd')

    @classmethod
    async def hset(cls, name, key, value, exp_of_none=None):
        assert cls.r, 'must call init first'
        return await cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback='hset')

    @classmethod
    async def hincrby(cls, name, key, value=1, exp_of_none=None):
        assert cls.r, 'must call init first'
        return await cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback='hincrby')

    @classmethod
    async def hincrbyfloat(cls, name, key, value, exp_of_none=None):
        assert cls.r, 'must call init first'
        return await cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback='hincrbyfloat')

    @classmethod
    async def incrby(cls, name, value=1, exp_of_none=None):
        assert cls.r, 'must call init first'
        return await cls._exp_of_none(name, value, exp_of_none=exp_of_none, callback='incrby')

    @classmethod
    async def close(cls):
        cls.r.close()
        await cls.r.wait_closed()


class RedisUtil:
    """
    封装缓存方法
    """
    r = None

    @classmethod
    def init(cls, conn=None, host='127.0.0.1', port=6379, password='', db=0, **kwargs):
        if conn:
            cls.r = conn  # type:redis.Redis
        else:
            pool = redis.ConnectionPool(host=host, port=port, password=password, db=db, **kwargs)
            cls.r = redis.Redis(connection_pool=pool)

    @classmethod
    def _exp_of_none(cls, *args, exp_of_none, callback):
        if not exp_of_none:
            return getattr(cls.r, callback)(*args)
        with cls.r.pipeline() as pipe:
            count = 0
            while True:
                try:
                    fun = getattr(pipe, callback)
                    key = args[0]
                    pipe.watch(key)
                    exp = pipe.ttl(key)
                    pipe.multi()
                    if exp == -2:
                        fun(*args)
                        pipe.expire(key, exp_of_none)
                        ret, _ = pipe.execute()
                    else:
                        fun(*args)
                        ret = pipe.execute()[0]
                    return ret
                except WatchError:
                    if count > 3:
                        raise WatchError
                    count += 1
                    continue

    @classmethod
    def get_or_set(cls, key, default=None, value_fun=None):
        """
        获取或者设置缓存
        """
        value = cls.r.get(key)
        if value is None and default:
            return default
        if value is not None:
            return value
        if value_fun:
            value, exp = value_fun()
            cls.r.set(key, value, exp)
        return value

    @classmethod
    def get(cls, key, default=None):
        value = cls.r.get(key)
        if value is None:
            return default
        return value

    @classmethod
    def set(cls, key, value, exp=None):
        """
        设置缓存
        """
        return cls.r.set(key, value, exp)

    @classmethod
    def delete(cls, key):
        """
        缓存清除，接收list or str
        """
        return cls.r.delete(key)

    @classmethod
    def sadd(cls, name, values, exp_of_none=None):
        return cls._exp_of_none(name, values, exp_of_none=exp_of_none, callback='sadd')

    @classmethod
    def hset(cls, name, key, value, exp_of_none=None):
        return cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback='hset')

    @classmethod
    def hincrby(cls, name, key, value=1, exp_of_none=None):
        return cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback='hincrby')

    @classmethod
    def hincrbyfloat(cls, name, key, value, exp_of_none=None):
        return cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback='hincrbyfloat')

    @classmethod
    def incrby(cls, name, value=1, exp_of_none=None):
        return cls._exp_of_none(name, value, exp_of_none=exp_of_none, callback='incrby')

    @classmethod
    def hget(cls, name, key, default=0):
        """
        缓存清除，接收list or str
        """
        v = cls.r.hget(name, key)
        if v is None:
            return default
        return v