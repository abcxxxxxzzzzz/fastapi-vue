from pydantic import BaseModel, Field, validator
from typing import Optional,List
from api.utils import is_valid_phone_number





class CreateIphoneNumberSchema(BaseModel):
    number: str = Field(..., title='手机号码', description='手机号码必须是11位')


    @validator('number')
    def validate_number(cls, val):
        '''校验'''
        if not is_valid_phone_number(val):
            raise ValueError(f'{val} 不合法')
        return val


class batchIphoneNumberSchema(BaseModel):
    ids: Optional[List] = []




class batchImportIphoneNumberSchema(BaseModel):
    importData: Optional[List] = []