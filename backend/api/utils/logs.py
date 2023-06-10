import logging
import time
import os

log_path = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_access = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_access.log')


logger = logging.getLogger()
logger.setLevel(logging.INFO)


ch = logging.StreamHandler()
fh = logging.FileHandler(filename=log_path_access)
formatter = logging.Formatter(
    # "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
    "%(asctime)s - [ %(threadName)s:%(funcName)s:%(lineno)d ] - %(levelname)s - %(message)s"
)


ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)      #将日志输出至屏幕
logger.addHandler(fh)      #将日志输出至文件


logger = logging.getLogger(__name__)

