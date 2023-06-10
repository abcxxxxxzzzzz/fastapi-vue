from fastapi import FastAPI,WebSocket
from api.routers import init_router
from api.configs.docs_conf import docs
from api.configs.config import global_settings
from api.exts import create_start_app_handler, create_stop_app_handler
from fastapi.middleware.cors import CORSMiddleware
# from api.exts import ApiExceptionHandler
from starlette.staticfiles import StaticFiles
import os
import pathlib

class FastApiApp:
    application = FastAPI(
        title        = docs.TITLE,
        description  = docs.DESC,
        version      = 'v1.0.0',
        debug        = False, # debug 是否再返回结果里面显示错误异常信息
        docs_url     = docs.DOCS_URL,
        openapi_url  = docs.OPENAPI_URL,
        redoc_url    = docs.REDOC_URL,
        openapi_tags = docs.TAGS_METADATA,
        servers      = docs.SERVERS,
    )
    

    def __init__(self):
        self.register_global_exception()         # 注册全局异常捕获信息
        self.register_global_cors()              # 全局配置跨域设置
        self.register_global_middleware()        # 注册全局中间件的注册
        self.register_global_event()             # 注册全局的启动和关闭事件
        self.register_global_ext_plugs()         # 注册所有自定义的或者第三的扩展插件
        self.register_global_websocket_router()  # 注册websocketAPI
        self.register_global_include_router()    # 批量导入注册路由
        self.register_upload()
        self.register_down()
        # self.mount_static_files()





    def register_global_event(self):
        ''' 全局时间启动和关闭事件 '''
        self.application.add_event_handler("startup", create_start_app_handler(self.application))
        self.application.add_event_handler("shutdown", create_stop_app_handler(self.application))


    def register_global_include_router(self):
        ''' 导入路由模块 '''
        init_router(self.application)


    def register_global_ext_plugs(self):
        ''' 初始化插件 '''
        pass


    def register_global_cors(self):
        ''' 处理全局的跨域 '''

        
        origins = [
            "http://127.0.0.1",
            "*"
        ]

        self.application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def register_global_middleware(self):
        ''' 配置中间件;先后顺序执行 '''
        # from api.utils.logs import logger
        import random
        import string
        import time


        app = self.application

        @app.middleware("http")
        async def log_requests(request, call_next):
            idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # logger.info(f"rid={idem} start request path={request.url.path}")
            start_time = time.time()
        
            response = await call_next(request)
            
            process_time = (time.time() - start_time) * 1000
            formatted_process_time = '{0:.2f}'.format(process_time)
            # logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
            return response


    def register_global_exception(self):
        ''' 配置自定义的异常 '''
        from starlette.exceptions import HTTPException as StarletteHTTPException
        from fastapi.exceptions import RequestValidationError
        from api.exts.init_exceptions import http_exception_handler, validation_exception_handler
        
        self.application.add_exception_handler(StarletteHTTPException, http_exception_handler)
        self.application.add_exception_handler(RequestValidationError, validation_exception_handler)




    def mount_static_files(self):
        ''' 装载静态目录,静态文件目录 '''
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        self.application.mount("/static", StaticFiles(directory=STATIC_DIR))



    def register_upload(self):
        '''API上传目录'''
        upload_name = global_settings.upload_name
        upload_path = global_settings.upload_path
        path = pathlib.Path(upload_name)
        if not path.exists():
            path.mkdir()
        
        self.application.mount(upload_path, StaticFiles(directory=upload_name), name=upload_name)


    def register_down(self):
        '''API下载目录'''
        down_name = global_settings.down_name
        down_path = global_settings.down_path
        path = pathlib.Path(down_name)
        if not path.exists():
            path.mkdir()

        self.application.mount(down_path, StaticFiles(directory=down_name), name=down_name)
            


    def register_global_websocket_router(self):

        ''' 全局 WebSocket 设置 '''
        app = self.application

        @app.websocket("/nw/websocket/{userid}")
        async def websocket_userid(websocket: WebSocket, userid: str):
            # 等待连接
            await websocket.accept()
            # 处理链接
            while True:
                # 接收发送过来的数据信息
                data = await websocket.receive_text()
                # 把接收过来的数据再一次的发送回去
                await websocket.send_text(f"ok")
                # 如果存在参数信息



