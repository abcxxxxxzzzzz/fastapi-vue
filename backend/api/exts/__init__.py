
from api.exts.init_database import init_db,Base,SessionLocal,engine
from api.exts.init_redis import redis_pool
from api.exts.init_scheduler import start_scheduler,shutdown_scheduler, Schedule
# from api.exts.init_exceptions import *
from fastapi import FastAPI
from typing import Callable
from api.utils.logs import *






def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        logger.info("Starting up...")
        # ------------------------------------初始化数据库
        await  init_db()
        # ------------------------------------初始化REDIS链接
        app.state.redis = await redis_pool()     
        # ------------------------------------初始化任务调度器, RuntimeWarning: coroutine 'Scheduler.start' was never awaited
        await  start_scheduler()


    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        logger.info("Shutting down...")
        # ------------------------------------ 关闭Redis链接
        await app.state.redis.close()
        # ------------------------------------ 关闭初始化任务调度器
        await shutdown_scheduler()
    return stop_app