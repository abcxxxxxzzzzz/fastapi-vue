import asyncio
from typing import Any, Callable, Optional, Sequence, Union
from fastapi import HTTPException, Response


# def has_permission(code: str = Depends(oauth2_scheme)):
def has_permissions(code: Optional[str] = None):
    print('验证权限标识',code)
    # 验证权限标识
    if not code:
        raise  HTTPException(status_code=403, detail='权限不足')
    # return   '验证权限标识返回'
    return object






from functools import wraps
from fastapi import Request, Depends,Header
from fastapi.security import OAuth2PasswordBearer
from api.services.LoginService import LoginCrud
from api.dependen import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from api.utils import getFromRedis
import json

# 自定义全局认证装饰器



def require_token(code: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            request = kwargs.get('request')
            fromRedis = await getFromRedis(request, current_user.username)

            if not fromRedis or fromRedis is None:
                raise HTTPException(status_code=401, detail='令牌失效')

            # print(code)
            # print(json.loads(fromRedis).get('permissions'))
            if code and code not in  json.loads(fromRedis).get('permissions'):
                raise HTTPException(status_code=403, detail='权限不足')
            return await func(*args, **kwargs)
        return wrapper
    return decorator