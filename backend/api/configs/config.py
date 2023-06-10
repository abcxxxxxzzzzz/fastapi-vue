import os
from functools import lru_cache
from api.utils import get_logger
from pydantic import BaseSettings
from typing import Optional



logger = get_logger(__name__)



class Settings(BaseSettings):
    """

    BaseSettings, from Pydantic, validates the data so that when we create an instance of Settings,
     environment and testing will have types of str and bool, respectively.

    Parameters:
    pg_user (str):
    pg_pass (str):
    pg_database: (str):
    pg_test_database: (str):
    asyncpg_url: AnyUrl:
    asyncpg_test_url: AnyUrl:

    Returns:
    instance of Settings

    """

    db_user: str = os.getenv("DB_USER", "")
    db_pass: str = os.getenv("DB_PASS", "")
    db_host: str = os.getenv("DB_HOST", "")
    db_port: str = os.getenv("DB_PORT", "") 
    db_name: str = os.getenv("DB_NAME", "")


    redis_pass: str = os.getenv("REDIS_PASS", "")
    redis_host: str = os.getenv("REDIS_HOST", "")
    redis_port: str = os.getenv("REDIS_PORT", "")
    redis_db:   str = os.getenv("REDIS_DB", 0)

    # token 相关配置
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")       # 加密密钥，用 uuid.uuid4().hex 生成的32位字符串
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "")         # 加密算法
    jwt_expire_minutes: int = os.getenv("JWT_EXPIRATION_TIME_MINUTES", 8640000)  # access token 过期时间，单位：分钟

    # 上传图片相关
    upload_name: str = os.getenv("UPLOAD_NAME", "upload")
    upload_path: str = os.getenv("UPLOAD_PATH", "/upload")


    # 保存文件相关
    down_name: str = os.getenv("UPLOAD_NAME", "donwload")
    down_path: str = os.getenv("UPLOAD_PATH", "/donwload")



    class Config:
            env_file = '.env'
            env_file_encoding = 'utf-8'

 

@lru_cache
def get_settings():
    logger.info("Loading config settings from the environment...")
    return Settings()



global_settings = get_settings()