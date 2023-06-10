import sqlalchemy
from api.configs.config import global_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# DATABASE_URL = "sqlite:///./fastapi.db"
# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )

DATABASE_URL = f"mysql+mysqlconnector://{global_settings.db_user}:{global_settings.db_pass}@{global_settings.db_host}:{global_settings.db_port}/{global_settings.db_name}"
metadata = sqlalchemy.MetaData()


engine = create_engine(
    DATABASE_URL,
    pool_recycle=60 * 5,  # 决定连接处于非活动状态后回收连接的秒数。默认值为 8 小时，默认值为 -1，表示不回收
    pool_pre_ping=True,   # 测试连接的活跃性,如果连接被MySQL回收但未被识别，将进行检查，并避免使用无效连接
    poolclass=NullPool,   # 保持长链接
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



async def init_db():
    Base.metadata.create_all(bind=engine)











# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import  sessionmaker,declarative_base
# from fastapi.encoders import jsonable_encoder
# from api.configs.config import global_settings
# from api.utils.logs import logger



# # global_settings = config.get_settings()
# # DATABASE_URL = global_settings.asyncdb_url


# ASYNC_DATABASE_URL: str =  (
#         # f"postgresql+asyncpg://{pg_user}:{pg_pass}@{pg_host}:5432/{pg_database}"
#         f"mysql+aiomysql://{global_settings.db_user}:{global_settings.db_pass}@{global_settings.db_host}:{global_settings.db_port}/{global_settings.db_name}?charset=utf8mb4"
#         # "sqlite+aiosqlite:///./fastapi.db"  
#     )


# # 如果您想使用不同的数据库（MySql、PostgreSQL 等），您需要安装支持 AsyncIO 的兼容驱动程序，并更新DATABASE_URL参数。
# # DATABASE_URL = "sqlite+aiosqlite:///./test.db"



# async_engine = create_async_engine(
#         ASYNC_DATABASE_URL, 
#         future=True, 
#         echo=True,
#         json_serializer=jsonable_encoder
#     )

# AsyncSessionFactory = sessionmaker(
#         async_engine, expire_on_commit=False, class_=AsyncSession
#     )


# Base = declarative_base()




# async def init_db():
#     async with async_engine.begin() as conn:
#         logger.info(f"ASYNC Pool: Init create db table")
#         # await conn.run_sync(Base.metadata.drop_all) # 删除表
#         await conn.run_sync(Base.metadata.create_all)



