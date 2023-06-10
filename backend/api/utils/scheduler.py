from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.cron import CronTrigger
import functools
import os
from redlock import RedLock, RedLockError
from api.configs import config

# 封装 Scheduler
class Scheduler(object):
    scheduler: AsyncIOScheduler = None


    @staticmethod
    def init(scheduler):
        Scheduler.scheduler = scheduler

    @staticmethod
    def configure(**kwargs):
        Scheduler.scheduler.configure(**kwargs)


    @staticmethod
    async def start():
        Scheduler.scheduler.start()


    @staticmethod
    def add(**kwargs):
        pass


    @staticmethod
    def edit():
        pass

    @staticmethod
    def pause(id, status):
        """
        暂停或恢复测试计划, 会影响到next_run_at
        :param plan_id:
        :param status:
        :return:
        """
        if status:
            Scheduler.scheduler.resume_job(job_id=str(id))
        else:
            Scheduler.scheduler.pause_job(job_id=str(id))

    @staticmethod
    def remove(id):
        Scheduler.scheduler.remove_job(id)

    @staticmethod
    def list():
        job_list = Scheduler.scheduler.get_jobs()
        return job_list


    @staticmethod
    async def shutdown():
        Scheduler.scheduler.shutdown(wait=False) # 将 wait 选项设置为 False 可以立即关闭。



    ## 计划任务分布式锁
    @staticmethod
    def lock(key):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    # 使用语句/上下文管理器， 试图获取分布式锁，如果没有获取到则会抛出RedLockError，所以我们这里捕获它
                    # 关于唯一key的确认，我这边首先加上了distributed_lock的前缀，是因为方便区分其他key，接着通过函数名称+唯一key确认分布式key，
                    # 但由于有的方法是带参数的，所以我选择再加一个args，来支持那些同方法不同参数的任务。
                    # 只需要在方法加上 lock 这个装饰器即可
                    with RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}", connection_details=config.get_settings().RedisCluster):
                        return await func(*args, **kwargs)
                except RedLockError:
                    print(f"进程: {os.getpid()}获取任务失败, 不用担心，还有其他哥们给你执行了")

            return wrapper

        return decorator
