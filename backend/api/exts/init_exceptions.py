import traceback
from fastapi import HTTPException
from pydantic import ValidationError
from pydantic.errors import *
from fastapi.exceptions import RequestValidationError
from api.utils import get_logger
from typing import Union
from starlette.requests import Request
from starlette.responses import Response
from api.utils.response import *



logger = get_logger(__name__)


class APIException(HTTPException):
    http_state_code = 500
    msg = '未知错误'
  
    def __init__(self, msg=None, http_state_code=http_state_code):
        if http_state_code:
            self.http_state_code = http_state_code
        if msg:
            self.msg = msg
        raise HTTPException(status_code=self.http_state_code, detail=self.msg)



async def http_exception_handler(request: Request, exc: APIException) -> Response:
    return ApiResponse(http_status_code=exc.status_code,code=exc.status_code, msg=exc.detail)




# 自定义请求有验证错误信息
err_msg = {
    'type_error.integer': '必须是数字',
    "value_error.missing": '不能为空',
    "type_error.list": '必须是数组',
    "type_error.bool": '必须是布尔类型',
    "value_error.any_str.min_length": '字符长度过短',
    "value_error.any_str.max_length": '字符长度过长',
    "value_error.jsondecode": '错误的类型',
    "value_error.number.not_le": "数据长度过大",
    "value_error.number.not_ge": "数据长度过小"
}


async def validation_exception_handler(
            request: Request, 
            exc: Union[RequestValidationError, ValidationError]
        ):

    logger.error(f'{exc.body} --> {[err.get("loc") for err in exc.errors()]}')

    status_code = getattr(exc, 'status_code', 400)

    msg = ""
    for err in exc.errors():
        print('错误字段:', err.get('loc')[-1])
        print('错误类型:', err.get('type'))
        print('错误信息:', err.get('msg'))

        _loc = err.get('loc')
        _type = err_msg.get(err.get('type'),err.get('msg'))
        if len(_loc) == 1:
            msg = '请求参数不能为空'
        elif _type:
            msg = _loc[-1] + " " + _type
        else:
            msg = err.get('msg')

    return ApiResponse(http_status_code=status_code,code=status_code, msg=msg)



# async def runtime_exception_handler(
#         request: Request, exc: Exception
# ) -> Response:
#     logger.debug(traceback.format_exc())
#     return ApiResponse()
