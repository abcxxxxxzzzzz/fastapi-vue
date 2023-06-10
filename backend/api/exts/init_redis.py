import aioredis
from api.configs.config import global_settings


# global_settings = config.get_settings()

# print(global_settings.dict())

# REDIS_URL = global_settings.asyncred_url
ASYNC_REDIS_URL: str= (
        f"redis://:{global_settings.redis_pass}@{global_settings.redis_host}:{global_settings.redis_port}/{global_settings.redis_db}?encoding=utf-8&decode_responses=True"
    )


async def redis_pool(db: int=0):
    '''
    redis链接池
    :return
    '''

    redis = await aioredis.from_url(
        # redis://[[username]:[password]]@localhost:6379/0
        # f"redis://:{redis_config.get('password')}@{redis_config.get('host')}/{db}?encoding=utf-8"
        # redis://127.0.0.1", port=44117, password='qwaszx', db=2, encoding="utf-8", decode_responses=True
        ASYNC_REDIS_URL
    )
    return redis

    