
# """

# 统一响应状态码

# """





# 自定义返回的错误的响应体信息
# ORJSONResponse一依赖于：orjson
from fastapi.responses import ORJSONResponse,JSONResponse
from typing import Any, Dict, Optional
import time
from fastapi.encoders import jsonable_encoder
from fastapi import status



class ApiResponse(JSONResponse):
    
    http_status_code = 200  # 定义返回响应码--如果不指定的话则默认都是返回200
    code = 0                # 默认成功
    data = None             # 结果可以是{} 或 []
    msg = '成功'

    def __init__(self,http_status_code=None, code=0, data=None,msg=None, **options):

        if code:
            self.code = code
        if data:
            self.data = data
        if msg:
            self.msg = msg

        if http_status_code:
            self.http_status_code = http_status_code

        # 返回内容体
        body = dict(
            msg=self.msg,
            code=self.code,
            data=self.data,
        )
        super(ApiResponse, self).__init__(status_code=self.http_status_code, content=body, **options)




class BadrequestException(ApiResponse):
    http_status_code  = 400
    code = 10032
    msg = '错误的请求'


class ParameterException(ApiResponse):
    http_status_code = 400
    code = 400
    msg = '参数校验错误,请检查提交的参数信息'
    


class UnauthorizedException(ApiResponse):
    http_status_code = 401
    code = 401
    msg = '未经许可授权'



class ForbiddenException(ApiResponse):
    http_status_code = 403
    msg = '失败！当前访问没有权限，或操作的数据没权限!'
    code = 403



class NotfoundException(ApiResponse):
    http_status_code = 404
    msg = '访问地址不存在'
    code = 404



class MethodnotallowedException(ApiResponse):
    http_status_code = 405
    msg = '不允许使用此方法提交访问'
    code = 405



class FileTooLargeException(ApiResponse):
    http_status_code = 413
    code = 413
    msg = '文件体积过大'


class FileTooManyException(ApiResponse):
    http_status_code = 414
    msg = '文件数量过多'
    code = 414


class FileExtensionException(ApiResponse):
    http_status_code = 415
    msg = '文件扩展名不符合规范'
    code = 415



class LimiterResException(ApiResponse):
    http_status_code = 429
    code = 429
    msg = '访问的速度过快'



class OtherException(ApiResponse):
    http_status_code = 800
    code = 800
    msg = '未知的其他HTTPEOOER异常'
    error_code = 10034



class InternalErrorException(ApiResponse):
    http_status_code = 500
    code = 500
    data = None
    msg = ' 服务崩溃异常'



class Success(ApiResponse):
    http_status_code = 200
    code = 200
    data = None  # 结果可以是{} 或 []
    msg = 'ok'



class Fail(ApiResponse):
    http_status_code = 200
    code = 200
    data = None  # 结果可以是{} 或 []
    msg = 'error'








class NotVerified(Exception):
    pass


class UserNotFound(Exception):
    pass
