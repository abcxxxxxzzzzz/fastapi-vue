import functools
import os
from redlock import RedLock, RedLockError
from api.configs.config import global_settings
from api.utils.logs import logger


connection_details=[
    {'host': global_settings.redis_host, 'port': global_settings.redis_port, 'db': global_settings.redis_db, 'password': global_settings.redis_pass}
]

    

def lock(key):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # print(func.__name__, key, args)
                # 试图获取分布式锁，如果没有获取到则会抛出RedLockError，所以我们这里捕获它
                with RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}",
                             connection_details=connection_details,
                             ):
                    return await func(*args, **kwargs)
            except RedLockError:
                logger.debug(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")
                print(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")

        return wrapper

    return decorator