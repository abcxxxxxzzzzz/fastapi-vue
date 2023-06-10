#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   文件名称 :     docs_conf
   文件功能描述 :   功能描述
   创建人 :       小钟同学
   创建时间 :          2021/6/9
-------------------------------------------------
   修改描述-2021/6/9:
   # starlette原生
        :param debug: debug模式
        :param middleware: 中间件列表
        :param exception_handlers: 异常对应处理的字典
        :param on_startup: 启动项列表
        :param on_shutdown: 结束项列表
        :param routes: 路由列表

        # OpenAPI文档相关
        :param docs_url: API文档地址
        :param title: 标题
        :param description: 描述
        :param version: API版本
        :param openapi_url: openapi.json的地址
        :param openapi_tags: 上述内容的元数据模式

        # 文档的页面中的OAuth，有关JS，以后介绍
        :param swagger_ui_oauth2_redirect_url:
        :param swagger_ui_init_oauth:

        # Redoc文档
        :param redoc_url: 文档地址

        # 反向代理情况下的文档
        :param servers: 服务器列表
        :param openapi_prefix: 支持反向代理和挂载子应用程序，已被弃用
        :param root_path: 如果有反向代理，让app直到自己"在哪"
        :param root_path_in_servers: 允许自动包含root_path

        :param default_response_class: 默认的response类
        :param extra:
-------------------------------------------------
"""
from functools import lru_cache
from pydantic import BaseSettings
import pprint

pp = pprint.PrettyPrinter(indent=4)


class DocsSettings(BaseSettings):
    """配置类"""
    API_V1_STR: str = ""
    # 文档接口描述相关的配置
    DOCS_URL = API_V1_STR + '/docs'
    REDOC_URL = API_V1_STR + '/redocs'
    # OPENAPI_URL配置我们的openapi，json的地址
    OPENAPI_URL = API_V1_STR + '/openapi_url'
    # 接口描述
    TITLE = "管理系统后台"
    # 首页描述文档的详细介绍信息
    DESC = """
            `线上预约系统`
            - 前端：使用 Vue + Vite 的框架进行搭建
            - 后端: 同步模式的多线程模式+ 单线程模式的协程模式
            - 技术栈: FastAPI + Sqlalchemy + ioredis + Vite 
        """
    TAGS_METADATA = [
        {
            "name": "后台管理系统",
            "description": "后台所有的公司的相关的权限管理",
        },
    ]
    # 配置代理相关的参数信息
    SERVERS = [
        {"url": "/", "description": "本地调试环境"},
        # {"url": "https://xx.xx.com", "description": "线上测试环境"},
        # {"url": "https://xx2.xx2.com", "description": "线上生产环境"},
    ]


@lru_cache()
def get_settings():
    return DocsSettings()


# 配置实例的对象的创建
docs = get_settings()
