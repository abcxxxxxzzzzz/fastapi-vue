from fastapi import Request
from typing import Optional


async def setToRedis(request: Request, key: str, value: str, expire: Optional[int] = 0):
    if expire:
        await request.app.state.redis.set(key, value, ex=expire)
    else:
        await request.app.state.redis.set(key, value)


async def getFromRedis(request: Request, key: str):
    return await request.app.state.redis.get(key)



async def removeFromRedis(request: Request, key: str):
    return await request.app.state.redis.delete(key)