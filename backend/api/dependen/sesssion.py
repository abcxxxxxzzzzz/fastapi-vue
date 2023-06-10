# from collections.abc import AsyncGenerator
# from api.exts import AsyncSessionFactory, async_engine
# from api.utils.logs import logger


# # Dependency
# async def get_session() -> AsyncGenerator:
#     async with AsyncSessionFactory() as session:
#         logger.debug(f"ASYNC Pool: {async_engine.pool.status()}")
#         yield session

from api.exts import SessionLocal
from sqlalchemy.orm import scoped_session 

def get_db():
    # db = SessionLocal()
    db = scoped_session(SessionLocal) # 是否已经创建Session，未创建则创建 Session
    try:
        yield db
    finally:
        db.close()