from pydantic import BaseModel
from typing import Union,List, Optional


class CreateMemberProfileSchema(BaseModel):
    code: Union[str, None] = None
    account: Union[str, None] = None
    account_id: Union[str, None] = None
    realname: Union[str, None] = None
    iphone_num: Union[str, None] = None
    contact: Union[str, None] = None
    bank_number: Union[str, None] = None
    description: Union[str, None] = None
    tag_id: Optional[List] = []
    owner_id: int





class batchImportMemberProfileSchema(BaseModel):
    importData: Optional[List] = []
