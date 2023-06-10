from pydantic import BaseModel
from typing import Optional,List,Union
from datetime import datetime,time


class CreateMemberSchema(BaseModel):
    username: str
    channel_code: Optional[str] = None
    description: Optional[str] = None
    # tags: Optional[List] = []
    tag_id: Optional[List] = []
    owner_id: int
    total_in_money: Union[int, float] = 0
    total_out_money: Union[int, float] = 0
    total_before_two_in_money: Union[int, float] = 0
    total_before_two_throw_money: Union[int, float] = 0
    total_before_two_out_money: Union[int, float] = 0
    # total_before_two_wax_money: Union[int, float] = 0
    # total_wax_money: Union[int, float] = 0
    register_at: Union[str, None] = None
    last_login_at: Union[str, None] = None
    register_ip: Optional[str] = None
    last_login_ip: Optional[str] = None


class multideleteMemberSchema(BaseModel):
    ids: Optional[List] = []


class multiSearchMemberSchema(BaseModel):
    batchType: str
    batchContent: Union[List, str] = []
    includeDelete: int
    owner_id: Union[int, None] = None
    tag_id: Union[List, None] = None


class importDataSchema(BaseModel):
    importData: Optional[List] = []