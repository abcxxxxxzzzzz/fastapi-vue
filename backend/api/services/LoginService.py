import time
from typing import Any, Union,Optional
from api.models import User
import jwt
from datetime import datetime, timedelta
from api.configs.config import global_settings
from jose import JWTError, jwt
from fastapi import Depends, HTTPException,Header,Request
from sqlalchemy.orm import Session
from api.dependen import get_db
from api.utils import setToRedis, getFromRedis,removeFromRedis,verify_password
import json



JWT_SECRET_KEY     = global_settings.jwt_secret_key  # 密钥
JWT_ALGORITHM      = global_settings.jwt_algorithm  # 算法
JWT_EXPIRE_MINUTES = global_settings.jwt_expire_minutes




class TokenService:

    async def login(self, request: Request, db: Session ,username:str, password:str, code:str='', uuid:str=''):

        # print('进入登录页:',username,password)

        '''查询用户是否存在'''
        query = await self.by_form_username(username=username, db=db)
        
        '''查询用户是否有效'''
        if not query.status:
            raise HTTPException(status_code=401,detail='用户已停用')
        


        '''验证密码是否正确'''
        if not verify_password(password, query.password):
            raise HTTPException(status_code=401,detail='账户/密码错误')

        token = await self.create_token(request, query)
        return token
        

    async def logout(self, request: Request, key):
        '''退出登录，清除缓存里的 LoginUser'''
        await removeFromRedis(request , key)
        
        

    async def create_token(self, request, query):
        '''细化 loginUser 信息，返回 jwt token'''
        from fastapi.encoders import jsonable_encoder

        roles = []
        for r in query.roles:
            if r.status:
                roles.append({ 'id': r.id, 'name': r.name })


        permissions = []
        for i in query.roles:
            for c in i.permissions:
                if c.code and c.method and c.status:
                    permissions.append(f"{c.code},{c.method}")
        

        _loginUser = {
            'id': query.id, 
            "username": query.username,
            "roles": list(roles),
            "permissions": permissions,
            "loginTime": time.time(),
        }

        # print(LoginUser(**_loginUser))
        token = await self.create_access_token(query.username)

        _loginUser['token'] = token
        await setToRedis(request,query.username, json.dumps(_loginUser), expire=JWT_EXPIRE_MINUTES*60)
        return token

    async def is_active(self, username,  db):
        query = await self.by_form_username(username=username, db=db)
        if not query:
            raise HTTPException(status_code=401, detail='用户不存在')
        elif not query.status:
            raise HTTPException(status_code=401, detail='用户已停用')
        return query


    async def verify_token(self, request: Request, token: Optional[str] =  Header(..., alias="X-Token"),  db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="无效的用户")
        except JWTError:
            raise HTTPException(status_code=401, detail="无效的凭据")

        # 从 Redis 获取用户数据并判断令牌是否失效
        fromRedisToken = await getFromRedis(request, username)
        if not fromRedisToken or json.loads(fromRedisToken).get('token') != token:
            raise HTTPException(status_code=401, detail="令牌失效")

        # 检查用户是否有效
        user = await self.is_active(username=username, db=db)
        return user


    async def create_access_token(self,  subject: Union[str, Any], expires_delta: timedelta = None
    ) -> str:
        '''创建 jwt token'''
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=JWT_EXPIRE_MINUTES     # 用户浏览器保存的 token 过期时间
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt


    async def by_form_username(self, username, db):
        query = db.query(User).filter(User.username == username).first()
        if not query:
            raise HTTPException(status_code=403,detail='用户不存在')
        return query

    # async def refresh_token(self, LoginUser: LoginUser):
    #     '''刷新缓存里的 loginUser 的过期时间'''
    #     pass



LoginCrud = TokenService()