from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from api.utils import logger
from api.exts.init_database import DATABASE_URL
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from api.exts.init_redis import ASYNC_REDIS_URL
from apscheduler.jobstores.redis import RedisJobStore
from api.configs.config import global_settings

workers = multiprocessing.cpu_count() * 2 + 1


JOBS_KEY      = 'apscheduler.jobs'
RUN_TIMES_KEY = 'apscheduler.run_times'

REDIS_CONF = {
    "password": global_settings.redis_pass,
    "host": global_settings.redis_host,
    "port": global_settings.redis_port,
    "db": global_settings.redis_db
}


# Schedule = None
init_schedule = {
            # 配置存储器
            'jobstores': {
                # 'default': SQLAlchemyJobStore(url=DATABASE_URL),
                'default': RedisJobStore(jobs_key=JOBS_KEY, run_times_key=RUN_TIMES_KEY, **REDIS_CONF),
            },
            # 配置执行器,使用进程池调度
            'executors': {
                # 'default': ProcessPoolExecutor(workers),
                'default': ThreadPoolExecutor(max_workers=workers*2),
                'processpool': ProcessPoolExecutor(max_workers=workers)
            },
            # 创建 job 时的默认参数
            'job_defaults': {
                'coalesce': True,  # 如果系统因为某些原因没有执行任务，导致任务累计，为True只运行一次，False则累计的任务全部跑一遍
                'max_instances': workers, # 允许并发运行最大实例数
            },
            'timezone': 'Asia/Shanghai'
        }

Schedule = AsyncIOScheduler(**init_schedule)


async def start_scheduler():
    # global Schedule
    try:
        Schedule.start()
        logger.info("Created Schedule Object")   
    except Exception as e:
        logger.error(str(e))     
        logger.error("Unable to Create Schedule Object")       






async def shutdown_scheduler():
    # global Schedule
    try:
        Schedule.shutdown()
        logger.info("Disabled Schedule")
    except Exception as e:
        logger.error(str(e))     
        logger.error("Unable to Disabled Schedule Object")     
    